import pytest
from app.ml.face_shape_classifier import FaceShapeClassifier
from app.models.schemas import FaceMeasurements


def test_face_shape_classifier_shapes():
    classifier = FaceShapeClassifier()

    # Oval face proportions
    oval_m = FaceMeasurements(
        face_length=245.0,
        face_width=180.0,
        forehead_width=152.0,
        cheekbone_width=180.0,
        jaw_width=145.0,
        aspect_ratio=1.36
    )
    shape, conf = classifier.classify(oval_m)
    assert shape in ["Oval", "Heart"]
    assert conf >= 0.75

    # Round face proportions
    round_m = FaceMeasurements(
        face_length=200.0,
        face_width=190.0,
        forehead_width=160.0,
        cheekbone_width=190.0,
        jaw_width=150.0,
        aspect_ratio=1.05
    )
    shape, conf = classifier.classify(round_m)
    assert shape == "Round"

    # Square face proportions
    square_m = FaceMeasurements(
        face_length=210.0,
        face_width=190.0,
        forehead_width=180.0,
        cheekbone_width=190.0,
        jaw_width=185.0,
        aspect_ratio=1.11
    )
    shape, conf = classifier.classify(square_m)
    assert shape == "Square"
