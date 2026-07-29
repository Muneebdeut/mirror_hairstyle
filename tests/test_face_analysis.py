import numpy as np
import pytest
from app.services.face_analysis import FaceAnalysisService
from app.models.schemas import FaceMeasurements


def test_no_face_detection():
    service = FaceAnalysisService()
    # Create a blank black image
    blank_img = np.zeros((400, 400, 3), dtype=np.uint8)
    res = service.analyze_face(blank_img)
    
    assert res.face_detected is False
    assert res.face_count == 0
    assert res.error is not None
    assert "couldn't detect a face" in res.error.lower()


def test_synthetic_face_measurements():
    service = FaceAnalysisService()
    measurements = FaceMeasurements(
        face_length=240.0,
        face_width=175.0,
        forehead_width=150.0,
        cheekbone_width=175.0,
        jaw_width=140.0,
        aspect_ratio=1.37
    )
    shape, conf = service.face_classifier.classify(measurements)
    assert shape in ["Oval", "Round", "Square", "Heart", "Oblong"]
    assert 0.70 <= conf <= 1.0
