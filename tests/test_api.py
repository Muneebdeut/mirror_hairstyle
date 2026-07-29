import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_recommend_hairstyles_api():
    payload = {
        "face_shape": "Oval",
        "hairstyle_preference": "no_preference",
        "hair_length": "Medium",
        "hair_texture": "Straight"
    }
    response = client.post("/api/recommend-hairstyles", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5


def test_try_on_api_mock():
    # Create sample image bytes using Pillow
    img = Image.new("RGB", (300, 300), color="blue")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
    data = {"hairstyle_name": "Textured Crop", "prompt_hint": "short crop"}

    response = client.post("/api/try-on", files=files, data=data)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert "data:image/jpeg;base64," in res_json["tryon_image_url"]
