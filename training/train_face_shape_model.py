"""
train_face_shape_model.py

Full 468-landmark training pipeline using MediaPipe + SVM on the Kaggle
'lucifierx/face-shape-classification' dataset.

Features used: all 468 normalised (x, y) landmark coordinates = 936-dim vector.
This gives far more discriminating power than hand-crafted ratios.
Class imbalance is handled via class_weight='balanced'.

Usage:
    python training/train_face_shape_model.py
"""

import os
import sys
import pickle
import math
import warnings
warnings.filterwarnings("ignore")

import cv2
import numpy as np
import mediapipe as mp
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# ─────────────────────────────────────────────────────────────────────────────
DATASET_ROOT = (
    r"C:\Users\munee\.cache\kagglehub\datasets"
    r"\lucifierx\face-shape-classification\versions\1\face shape detector"
)

LABEL_MAP = {
    "oval":     "Oval",
    "round":    "Round",
    "square":   "Square",
    "heart":    "Heart",
    "oblong":   "Oblong",
    "diamond":  "Heart",    # similar wide-forehead narrow-chin profile
    "triangle": "Heart",
}

MODEL_OUTPUT = os.path.join(
    os.path.dirname(__file__), "..", "backend", "app", "ml", "face_shape_model.pkl"
)

mp_face_mesh = mp.solutions.face_mesh


# ─────────────────────────────────────────────────────────────────────────────
def extract_raw_landmarks(img_bgr: np.ndarray):
    """
    Returns a 936-dim vector of all 468 normalised (x, y) landmark coords,
    normalised to face bounding box so it is scale/position-invariant.
    Returns None if no face is found.
    """
    h, w = img_bgr.shape[:2]
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.3,
    ) as fm:
        res = fm.process(rgb)

    if not res.multi_face_landmarks:
        return None

    lm = res.multi_face_landmarks[0].landmark
    xs = np.array([p.x for p in lm])
    ys = np.array([p.y for p in lm])

    # Normalise to [0,1] within the face bounding box
    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()
    xr = xmax - xmin if xmax != xmin else 1.0
    yr = ymax - ymin if ymax != ymin else 1.0
    xs = (xs - xmin) / xr
    ys = (ys - ymin) / yr

    return np.concatenate([xs, ys])  # shape (936,)


def extract_ratio_features(img_bgr: np.ndarray):
    """
    6-dim hand-crafted geometric ratio feature vector (secondary).
    """
    h, w = img_bgr.shape[:2]
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.3,
    ) as fm:
        res = fm.process(rgb)

    if not res.multi_face_landmarks:
        return None

    lm = res.multi_face_landmarks[0].landmark
    def pt(i): return lm[i].x * w, lm[i].y * h
    def d(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])

    top = pt(10); chin = pt(152)
    lc = pt(234); rc = pt(454)
    lf = pt(103); rf = pt(332)
    lj = pt(172); rj = pt(397)

    fh  = d(top, chin) * 1.15
    cw  = d(lc, rc)
    fw  = d(lf, rf)
    jw  = d(lj, rj)
    ew  = fw * 0.60
    eps = 1e-6

    return np.array([
        fh / max(cw, eps),
        jw / max(cw, eps),
        fw / max(cw, eps),
        fw / max(jw, eps),
        ew / max(cw, eps),
        (cw - jw) / max(fh, eps),
    ])


# ─────────────────────────────────────────────────────────────────────────────
def load_dataset():
    X_lm, X_rat, y = [], [], []
    skipped = 0

    for folder, label in LABEL_MAP.items():
        folder_path = os.path.join(DATASET_ROOT, folder)
        if not os.path.isdir(folder_path):
            continue

        files = [f for f in os.listdir(folder_path)
                 if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

        for fname in files:
            img = cv2.imread(os.path.join(folder_path, fname))
            if img is None:
                skipped += 1
                continue

            # Try original size first, then 640×640
            lm = extract_raw_landmarks(img)
            rat = extract_ratio_features(img)
            if lm is None:
                big = cv2.resize(img, (640, 640))
                lm  = extract_raw_landmarks(big)
                rat = extract_ratio_features(big)

            if lm is None:
                skipped += 1
                continue

            X_lm.append(lm)
            X_rat.append(rat)
            y.append(label)

    print(f"Loaded {len(X_lm)} samples | Skipped: {skipped}")
    counts = {}
    for lbl in y:
        counts[lbl] = counts.get(lbl, 0) + 1
    print("Class distribution:", counts)

    # Concatenate landmark + ratio features
    X = np.concatenate([
        np.array(X_lm,  dtype=np.float64),
        np.array(X_rat, dtype=np.float64),
    ], axis=1)

    return X, np.array(y)


# ─────────────────────────────────────────────────────────────────────────────
def train_and_save():
    print("=" * 62)
    print("  Face Shape Classifier - Full Landmark Training Pipeline")
    print("=" * 62)

    X, y = load_dataset()
    n_splits = min(5, min(
        sum(1 for lbl in y if lbl == c) for c in set(y)
    ))

    candidates = {
        "SVM-RBF (C=5)": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", SVC(kernel="rbf", C=5, gamma="scale",
                        probability=True, class_weight="balanced",
                        random_state=42)),
        ]),
        "SVM-RBF (C=20)": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", SVC(kernel="rbf", C=20, gamma="scale",
                        probability=True, class_weight="balanced",
                        random_state=42)),
        ]),
        "RandomForest": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=600, max_depth=None,
                class_weight="balanced", random_state=42)),
        ]),
    }

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    best_name, best_model, best_score = None, None, -1.0

    for name, pipe in candidates.items():
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        mean = scores.mean()
        print(f"  {name:<25s}  CV Acc: {mean*100:.1f}% +/- {scores.std()*100:.1f}%")
        if mean > best_score:
            best_score, best_name, best_model = mean, name, pipe

    print(f"\nBest: {best_name}  (CV Acc: {best_score*100:.1f}%)")

    # Hold-out evaluation
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    best_model.fit(X_tr, y_tr)
    y_pred = best_model.predict(X_te)

    print("\n" + "=" * 62)
    print("  HOLD-OUT EVALUATION")
    print("=" * 62)
    print(f"  Accuracy: {accuracy_score(y_te, y_pred)*100:.1f}%\n")
    print(classification_report(y_te, y_pred))

    # Retrain on all data and save
    best_model.fit(X, y)
    os.makedirs(os.path.dirname(os.path.abspath(MODEL_OUTPUT)), exist_ok=True)
    with open(MODEL_OUTPUT, "wb") as f:
        pickle.dump(best_model, f)
    print(f"Model saved -> {os.path.abspath(MODEL_OUTPUT)}")
    print("=" * 62)


if __name__ == "__main__":
    train_and_save()
