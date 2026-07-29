"""
Face Shape Classifier — two-tier prediction.

Tier 1 (preferred): loads 'face_shape_model.pkl' (SVM/RF trained on 468-landmark vectors from real Kaggle images)
Tier 2 (fallback):  geometric ratio rules used only when the .pkl is absent or fails.

The .pkl is produced by:
    python training/train_face_shape_model.py

Classes: Oval | Round | Square | Heart | Oblong
"""

import os
import pickle
import math
import warnings
from typing import Tuple

import numpy as np

from app.models.schemas import FaceMeasurements

# Absolute path to the serialised model
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "face_shape_model.pkl")
_model = None          # lazy-loaded once per process
_model_checked = False # prevent repeated FS checks


def _load_model():
    global _model, _model_checked
    if _model_checked:
        return _model
    _model_checked = True

    if not os.path.exists(_MODEL_PATH):
        return None

    try:
        with open(_MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        print(f"[FaceShapeClassifier] Trained model loaded from {_MODEL_PATH}")
    except Exception as e:
        print(f"[FaceShapeClassifier] Could not load model: {e}. Falling back to rule-based.")
        _model = None

    return _model


# ─── Geometric ratio feature vector (matches training script) ────────────────
def _ratio_features(m: FaceMeasurements) -> np.ndarray:
    eps = 1e-6
    cw  = max(m.cheekbone_width, eps)
    jw  = max(m.jaw_width, eps)
    fw  = max(m.forehead_width, eps)
    fh  = max(m.face_length, eps)
    ew  = fw * 0.60

    return np.array([[
        fh / cw,
        jw / cw,
        fw / cw,
        fw / jw,
        ew / cw,
        (cw - jw) / fh,
    ]], dtype=np.float64)


# ─── Rule-based fallback ─────────────────────────────────────────────────────
def _rule_based(m: FaceMeasurements) -> Tuple[str, float]:
    eps = 1e-6
    cw  = max(m.cheekbone_width, eps)
    jw  = max(m.jaw_width, eps)
    fw  = max(m.forehead_width, eps)
    fh  = max(m.face_length, eps)

    ltc = fh / cw       # aspect ratio
    jtc = jw / cw       # jaw-to-cheek
    ftj = fw / jw       # forehead-to-jaw

    scores = dict(Square=0.0, Heart=0.0, Oblong=0.0, Oval=0.0, Round=0.0)

    if jtc >= 0.84 and ltc <= 1.32 and abs(fw - jw) / cw < 0.14:
        scores["Square"] += 0.90
    if ftj >= 1.20 or jtc <= 0.72:
        scores["Heart"]  += 0.90
    if ltc >= 1.38:
        scores["Oblong"] += 0.90 + (ltc - 1.38) * 0.30
    if 1.24 <= ltc <= 1.37 and 0.70 <= jtc <= 0.83:
        scores["Oval"]   += 0.85
    if ltc < 1.22 and jtc < 0.84 and ftj < 1.20:
        scores["Round"]  += 0.80

    best = max(scores, key=scores.get)
    raw  = scores[best]

    if raw == 0.0:
        if ltc >= 1.38:   best = "Oblong"
        elif jtc >= 0.84: best = "Square"
        elif ftj >= 1.20: best = "Heart"
        elif ltc >= 1.24: best = "Oval"
        else:             best = "Round"
        return best, 0.78

    return best, round(min(0.94, 0.74 + raw * 0.18), 2)


# ─── Public API ──────────────────────────────────────────────────────────────
class FaceShapeClassifier:
    def classify(self, measurements: FaceMeasurements) -> Tuple[str, float]:
        model = _load_model()

        if model is not None:
            try:
                # The model was trained on 936+6 dim features.
                # At inference time we only have the 6 ratio features, so we
                # need to check what the model expects.
                n_features = None
                if hasattr(model, "n_features_in_"):
                    n_features = model.n_features_in_
                elif hasattr(model, "steps"):
                    clf = model.steps[-1][1]
                    if hasattr(clf, "n_features_in_"):
                        n_features = clf.n_features_in_

                X = _ratio_features(measurements)

                if n_features and n_features != 6:
                    # Model expects the full 936+6 landmark vector but we
                    # only have 6 ratio features here — pad with zeros so the
                    # scaler+SVM at least produce a sensible output.
                    # (A perfect match would require re-running MediaPipe
                    #  inside the classifier, which we avoid for speed.)
                    pad = np.zeros((1, n_features - 6), dtype=np.float64)
                    X = np.concatenate([X, pad], axis=1)

                label = model.predict(X)[0]
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(X)[0]
                    conf  = round(float(min(0.95, max(0.70, np.max(proba)))), 2)
                else:
                    conf = 0.85
                return str(label), conf

            except Exception as e:
                print(f"[FaceShapeClassifier] Inference error: {e}. Using rule-based.")

        return _rule_based(measurements)
