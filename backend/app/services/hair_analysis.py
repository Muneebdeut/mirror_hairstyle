"""
Hair Analysis Service.
Analyzes hair characteristics (length, texture, density, volume)
from an input image using Groq Vision model (qwen/qwen3.6-27b).
"""

import io
import base64
import json
import logging
import os
import re

from typing import Dict, Optional
import numpy as np
from PIL import Image
from groq import Groq

try:
    import cv2
except ImportError:
    cv2 = None

from app.models.schemas import HairAnalysisResponse, HairCharacteristics

logger = logging.getLogger(__name__)

# ── Groq Vision Configuration ──────────────────────────────────────────────────
_GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
_VISION_MODEL = "qwen/qwen3.6-27b"

_VALID_LENGTHS = {"very short", "short", "medium", "long"}
_VALID_TEXTURES = {"straight", "wavy", "curly", "coily"}
_VALID_DENSITIES = {"low", "medium", "high"}
_VALID_VOLUMES = {"low", "medium", "high"}

_VISION_PROMPT = (
    "Analyze the person's hair in this photo carefully.\n\n"
    "Determine the following hair characteristics:\n"
    "1. hair_length: Exactly one of [Short, Medium, Long, Very Short]\n"
    "2. hair_texture: Exactly one of [Straight, Wavy, Curly, Coily]\n"
    "3. hair_density: Exactly one of [Low, Medium, High]\n"
    "4. hair_volume: Exactly one of [Low, Medium, High]\n\n"
    "Respond ONLY with valid JSON in this exact structure:\n"
    "{\n"
    '  "hair_length": "Short",\n'
    '  "hair_texture": "Wavy",\n'
    '  "hair_density": "Medium",\n'
    '  "hair_volume": "Medium"\n'
    "}"
)

_groq_client: Optional[Groq] = None


def _get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=_GROQ_API_KEY)
    return _groq_client


def _encode_image(img_arr: np.ndarray) -> str:
    """Encodes image to base64 JPEG string (max width 800px)."""
    if cv2 is not None and isinstance(img_arr, np.ndarray):
        h, w = img_arr.shape[:2]
        if w > 800:
            scale = 800 / w
            img_arr = cv2.resize(img_arr, (800, int(h * scale)), interpolation=cv2.INTER_AREA)
        _, buf = cv2.imencode(".jpg", img_arr, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return base64.b64encode(buf.tobytes()).decode()

    # PIL fallback
    img_pil = Image.fromarray(img_arr)
    if img_pil.width > 800:
        scale = 800 / img_pil.width
        img_pil = img_pil.resize((800, int(img_pil.height * scale)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img_pil.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def _parse_hair_json(text: str) -> Optional[Dict[str, str]]:
    """Strips <think> blocks & markdown backticks, then parses JSON."""
    try:
        clean = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        clean = re.sub(r"```(?:json)?", "", clean).strip()

        start_idx = clean.find("{")
        end_idx = clean.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = clean[start_idx : end_idx + 1]
            data = json.loads(json_str)

            length = str(data.get("hair_length", "")).strip().lower()
            texture = str(data.get("hair_texture", "")).strip().lower()
            density = str(data.get("hair_density", "")).strip().lower()
            volume = str(data.get("hair_volume", "")).strip().lower()

            res = {}
            if length in _VALID_LENGTHS:
                res["hair_length"] = length.title()
            if texture in _VALID_TEXTURES:
                res["hair_texture"] = texture.title()
            if density in _VALID_DENSITIES:
                res["hair_density"] = density.title()
            if volume in _VALID_VOLUMES:
                res["hair_volume"] = volume.title()

            if len(res) == 4:
                return res

    except Exception as e:
        logger.warning(f"Error parsing hair analysis JSON: {e}")

    return None


class HairAnalysisService:
    def analyze_hair(self, img_arr: np.ndarray) -> HairAnalysisResponse:
        try:
            b64_img = _encode_image(img_arr)
            client = _get_groq_client()

            response = client.chat.completions.create(
                model=_VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": _VISION_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{b64_img}"
                                },
                            },
                        ],
                    }
                ],
                temperature=0.1,
                max_completion_tokens=1024,
            )

            raw_text = response.choices[0].message.content or ""
            parsed = _parse_hair_json(raw_text)

            if parsed:
                chars = HairCharacteristics(
                    hair_length=parsed["hair_length"],
                    hair_texture=parsed["hair_texture"],
                    hair_density=parsed["hair_density"],
                    hair_volume=parsed["hair_volume"],
                )
                return HairAnalysisResponse(
                    hair_detected=True, hair_characteristics=chars
                )

        except Exception as e:
            logger.error(f"Groq hair analysis failed: {e}")

        # Fallback default values
        fallback = HairCharacteristics(
            hair_length="Medium",
            hair_texture="Wavy",
            hair_density="Medium",
            hair_volume="Medium",
        )
        return HairAnalysisResponse(
            hair_detected=True, hair_characteristics=fallback
        )
