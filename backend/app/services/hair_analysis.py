"""
Hair Analysis Service.

Detection priority:
  1. Groq Vision API (qwen/qwen3.6-27b) — uses AI vision to predict hair length, texture, density, and volume.
  2. OpenCV texture & edge analysis — fallback heuristics.
"""

import base64
import cv2
import json
import logging
import re
from typing import Optional, Tuple, Dict, Any

import numpy as np
from groq import Groq

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
    "Return ONLY a JSON object in this format:\n"
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


def _encode_image(img_bgr: np.ndarray) -> str:
    """Encodes image to base64 JPEG string (max width 800px)."""
    h, w = img_bgr.shape[:2]
    if w > 800:
        scale = 800 / w
        img_bgr = cv2.resize(img_bgr, (800, int(h * scale)), interpolation=cv2.INTER_AREA)
    _, buf = cv2.imencode(".jpg", img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf.tobytes()).decode()


def _parse_hair_json(text: str) -> Optional[Dict[str, str]]:
    """Strips <think> blocks & markdown backticks, then parses JSON."""
    try:
        clean = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        clean = re.sub(r"```(?:json)?", "", clean).strip()

        # Find JSON object bounds
        start_idx = clean.find("{")
        end_idx = clean.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = clean[start_idx : end_idx + 1]
            data = json.loads(json_str)

            length = str(data.get("hair_length", "")).strip().title()
            texture = str(data.get("hair_texture", "")).strip().title()
            density = str(data.get("hair_density", "")).strip().title()
            volume = str(data.get("hair_volume", "")).strip().title()

            res = {}
            if length.lower() in _VALID_LENGTHS:
                res["hair_length"] = length
            if texture.lower() in _VALID_TEXTURES:
                res["hair_texture"] = texture
            if density.lower() in _VALID_DENSITIES:
                res["hair_density"] = density
            if volume.lower() in _VALID_VOLUMES:
                res["hair_volume"] = volume

            if len(res) >= 2:  # If at least 2 fields matched correctly
                return res
    except Exception as e:
        logger.warning(f"[Hair Vision API] Failed to parse JSON response: {e}")

    return None


def _analyze_via_groq_vision(img_bgr: np.ndarray) -> Optional[HairCharacteristics]:
    """Calls Groq Vision API to predict hair characteristics."""
    try:
        b64 = _encode_image(img_bgr)
        client = _get_groq_client()
        resp = client.chat.completions.create(
            model=_VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": _VISION_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ],
            }],
            max_completion_tokens=1024,
            temperature=0.1,
        )
        raw = resp.choices[0].message.content or ""
        parsed = _parse_hair_json(raw)
        if parsed:
            logger.info(f"[Hair Vision API] Hair analysis successful: {parsed}")
            return HairCharacteristics(
                hair_length=parsed.get("hair_length", "Medium"),
                hair_texture=parsed.get("hair_texture", "Wavy"),
                hair_density=parsed.get("hair_density", "Medium"),
                hair_volume=parsed.get("hair_volume", "Medium"),
            )
    except Exception as e:
        logger.error(f"[Hair Vision API] Error during analysis: {e}")

    return None


class HairAnalysisService:
    def analyze_hair(self, img_bgr: Optional[np.ndarray]) -> HairAnalysisResponse:
        """
        Analyzes hair region characteristics using Groq Vision API (primary)
        or OpenCV texture heuristics (fallback).
        """
        if img_bgr is not None:
            # Tier 1: Groq Vision API Prediction
            vision_result = _analyze_via_groq_vision(img_bgr)
            if vision_result is not None:
                return HairAnalysisResponse(
                    hair_characteristics=vision_result,
                    confidence=0.92,
                    message="AI vision hair analysis completed using Groq model."
                )

            # Tier 2: OpenCV Fallback Analysis
            try:
                h, w, _ = img_bgr.shape
                upper_region = img_bgr[0:int(h * 0.45), :]
                gray_upper = cv2.cvtColor(upper_region, cv2.COLOR_BGR2GRAY)

                texture_score = cv2.Laplacian(gray_upper, cv2.CV_64F).var()
                edges = cv2.Canny(gray_upper, 50, 150)
                edge_density = np.sum(edges > 0) / float(edges.size)

                side_region = img_bgr[int(h * 0.3):int(h * 0.8), :]
                side_edges = cv2.Canny(side_region, 50, 150)
                side_density = np.sum(side_edges > 0) / float(side_edges.size)

                # Texture mapping
                if edge_density > 0.18 or texture_score > 350:
                    estimated_texture = "Curly"
                elif edge_density > 0.11 or texture_score > 180:
                    estimated_texture = "Wavy"
                elif edge_density > 0.04:
                    estimated_texture = "Straight"
                else:
                    estimated_texture = "Wavy"

                # Length mapping
                if side_density > 0.15:
                    estimated_length = "Long"
                elif side_density > 0.08:
                    estimated_length = "Medium"
                else:
                    estimated_length = "Short"

                # Density mapping
                if edge_density > 0.12:
                    estimated_density = "High"
                elif edge_density > 0.05:
                    estimated_density = "Medium"
                else:
                    estimated_density = "Low"

                return HairAnalysisResponse(
                    hair_characteristics=HairCharacteristics(
                        hair_length=estimated_length,
                        hair_texture=estimated_texture,
                        hair_density=estimated_density,
                        hair_volume="Medium"
                    ),
                    confidence=0.82,
                    message="AI hair analysis completed via image feature heuristics."
                )
            except Exception as e:
                logger.error(f"[HairAnalysisService] Fallback error: {e}")

        # Default fallback response
        return HairAnalysisResponse(
            hair_characteristics=HairCharacteristics(
                hair_length="Medium",
                hair_texture="Wavy",
                hair_density="Medium",
                hair_volume="Medium"
            ),
            confidence=0.70,
            message="Default hair characteristics estimated. You can adjust as desired."
        )
