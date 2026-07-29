"""
Face Analysis Service.

Detection priority:
  1. Groq Vision API (qwen/qwen3.6-27b) — looks at the actual photo, most accurate
  2. ML model (RandomForest on 962-dim MediaPipe landmarks) — trained on Kaggle dataset
  3. Geometric ratio rules — pure math fallback

MediaPipe is always run to extract landmark measurements for the response payload.
"""

import base64
import cv2
import math
import re
import os
import logging
from typing import Optional, Tuple

import numpy as np
import mediapipe as mp
from groq import Groq

from app.models.schemas import FaceAnalysisResponse, FaceMeasurements
from app.ml.face_shape_classifier import FaceShapeClassifier, _load_model

logger = logging.getLogger(__name__)

# ── Groq vision config ────────────────────────────────────────────────────────
_GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
_VISION_MODEL  = "qwen/qwen3.6-27b"
_VALID_SHAPES  = {"oval", "round", "square", "heart", "oblong"}

_VISION_PROMPT = (
    "Analyze this face and determine the face shape. "
    "Look at: forehead width, cheekbone width, jawline width, and face length.\n\n"
    "Face shapes:\n"
    "- Oval: forehead slightly wider than jaw, gently tapered chin, longer than wide\n"
    "- Round: wide cheeks, soft rounded jaw, nearly as wide as long\n"
    "- Square: strong angular jaw, forehead and jaw similar width, angular not round\n"
    "- Heart: noticeably wider forehead narrowing sharply to a pointed chin\n"
    "- Oblong: significantly longer than wide, similar width top to bottom\n\n"
    "IMPORTANT: Respond with ONLY the face shape word and nothing else.\n"
    "Your answer must be exactly ONE of: Oval, Round, Square, Heart, Oblong"
)

_groq_client: Optional[Groq] = None


def _get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=_GROQ_API_KEY)
    return _groq_client


# ── Helper: encode image for Groq ─────────────────────────────────────────────
def _encode_image(img_bgr: np.ndarray) -> str:
    """Returns base64-encoded JPEG string."""
    # Resize to max 800px wide to keep payload small and fast
    h, w = img_bgr.shape[:2]
    if w > 800:
        scale = 800 / w
        img_bgr = cv2.resize(img_bgr, (800, int(h * scale)), interpolation=cv2.INTER_AREA)
    _, buf = cv2.imencode(".jpg", img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf.tobytes()).decode()


def _parse_shape_from_text(text: str) -> Optional[str]:
    """Extract and normalise the face shape word from model output."""
    # Strip <think> blocks (Qwen3 uses chain-of-thought)
    clean = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    # Find first valid shape word (case-insensitive)
    for token in re.split(r"[\s\W]+", clean):
        if token.lower() in _VALID_SHAPES:
            return token.capitalize()
    return None


# ── Groq Vision face-shape detection ─────────────────────────────────────────
def _classify_via_groq_vision(img_bgr: np.ndarray) -> Tuple[Optional[str], float]:
    """Call Groq qwen vision model. Returns (shape, confidence) or (None, 0)."""
    try:
        b64 = _encode_image(img_bgr)
        client = _get_groq_client()
        resp = client.chat.completions.create(
            model=_VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": _VISION_PROMPT},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ],
            }],
            max_completion_tokens=1024,  # qwen3 needs tokens for <think> block
            temperature=0.1,
        )
        raw = resp.choices[0].message.content or ""
        shape = _parse_shape_from_text(raw)
        if shape:
            logger.info(f"[Vision API] Detected face shape: {shape}")
            return shape, 0.92
        logger.warning(f"[Vision API] Could not parse shape from: {raw!r}")
        return None, 0.0
    except Exception as e:
        logger.error(f"[Vision API] Error: {e}")
        return None, 0.0


# ── MediaPipe ML fallback ─────────────────────────────────────────────────────
def _ml_classify(landmarks, measurements: FaceMeasurements) -> Tuple[Optional[str], float]:
    model = _load_model()
    if model is None:
        return None, 0.0
    try:
        xs = np.array([p.x for p in landmarks])
        ys = np.array([p.y for p in landmarks])
        xr = xs.max() - xs.min() or 1.0
        yr = ys.max() - ys.min() or 1.0
        xs = (xs - xs.min()) / xr
        ys = (ys - ys.min()) / yr
        lm_vec = np.concatenate([xs, ys])

        eps = 1e-6
        cw, jw, fw, fh = (max(v, eps) for v in [
            measurements.cheekbone_width, measurements.jaw_width,
            measurements.forehead_width, measurements.face_length,
        ])
        ratio_vec = np.array([
            fh/cw, jw/cw, fw/cw, fw/jw, (fw*0.6)/cw, (cw-jw)/fh,
        ])

        X = np.concatenate([lm_vec, ratio_vec]).reshape(1, -1).astype(np.float64)

        # Trim / pad to model's expected input size
        n_exp = getattr(model, "n_features_in_", None)
        if n_exp and X.shape[1] != n_exp:
            if X.shape[1] > n_exp:
                X = X[:, :n_exp]
            else:
                X = np.pad(X, [(0, 0), (0, n_exp - X.shape[1])])

        label = str(model.predict(X)[0])
        conf = 0.85
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            conf = round(float(min(0.92, max(0.70, float(np.max(proba))))), 2)
        return label, conf
    except Exception as e:
        logger.error(f"[ML Classify] Error: {e}")
        return None, 0.0


# ── Main service class ────────────────────────────────────────────────────────
class FaceAnalysisService:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_classifier = FaceShapeClassifier()

    def _run_mediapipe(self, img_bgr: np.ndarray):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
        ) as fm:
            return fm.process(img_rgb)

    def _extract_measurements(self, landmarks, w: int, h: int) -> FaceMeasurements:
        lm = landmarks

        def pt(i): return lm[i].x * w, lm[i].y * h
        def d(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])

        face_length    = d(pt(10), pt(152)) * 1.15
        cheekbone_w    = d(pt(234), pt(454))
        forehead_w     = d(pt(103), pt(332))
        jaw_w          = d(pt(172), pt(397))

        return FaceMeasurements(
            face_length     = round(face_length, 1),
            face_width      = round(cheekbone_w, 1),
            forehead_width  = round(forehead_w, 1),
            cheekbone_width = round(cheekbone_w, 1),
            jaw_width       = round(jaw_w, 1),
            aspect_ratio    = round(face_length / max(1.0, cheekbone_w), 2),
        )

    def analyze_face(self, img_bgr: np.ndarray) -> FaceAnalysisResponse:
        h, w = img_bgr.shape[:2]

        # ── STEP 1: Run MediaPipe to detect face & get measurements ───────
        results = self._run_mediapipe(img_bgr)

        if not results or not results.multi_face_landmarks:
            # Haar cascade last resort
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            if len(faces) == 0:
                return FaceAnalysisResponse(
                    face_detected=False, face_count=0,
                    error="We couldn't detect a face. Please upload a clear, front-facing photo."
                )

        if results.multi_face_landmarks and len(results.multi_face_landmarks) > 1:
            return FaceAnalysisResponse(
                face_detected=True, face_count=len(results.multi_face_landmarks),
                error="Please upload a photo containing only one person."
            )

        # Get measurements (for the response payload)
        measurements = None
        lm_list = None
        if results.multi_face_landmarks:
            lm_list = results.multi_face_landmarks[0].landmark
            measurements = self._extract_measurements(lm_list, w, h)

        # ── STEP 2: Classify face shape (Vision API → ML → Rules) ────────

        # Tier 1: Groq Vision API (most accurate — actually looks at the photo)
        shape, conf = _classify_via_groq_vision(img_bgr)

        # Tier 2: Trained ML model on 962-dim MediaPipe landmarks
        if shape is None and lm_list is not None and measurements is not None:
            shape, conf = _ml_classify(lm_list, measurements)

        # Tier 3: Geometric ratio rules
        if shape is None and measurements is not None:
            shape, conf = self.face_classifier.classify(measurements)

        # Absolute fallback
        if shape is None:
            shape, conf = "Oval", 0.70

        return FaceAnalysisResponse(
            face_detected=True,
            face_count=1,
            face_shape=shape,
            confidence=conf,
            measurements=measurements,
        )
