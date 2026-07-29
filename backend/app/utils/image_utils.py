import io
import base64
import cv2
import numpy as np
from PIL import Image
from typing import Tuple


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decode raw image bytes into an OpenCV BGR image numpy array."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image file or format could not be decoded.")
    return img


def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """Convert BGR OpenCV image to RGB."""
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def encode_image_to_base64_data_url(img_bgr: np.ndarray, format_ext: str = ".jpg") -> str:
    """Encode OpenCV BGR image to base64 data URL string."""
    success, buffer = cv2.imencode(format_ext, img_bgr)
    if not success:
        raise ValueError("Failed to encode image.")
    b64_str = base64.b64encode(buffer).decode("utf-8")
    mime_type = "image/jpeg" if format_ext.lower() in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime_type};base64,{b64_str}"


def resize_image_max_dim(img: np.ndarray, max_dim: int = 1024) -> np.ndarray:
    """Resize image so its maximum dimension does not exceed max_dim while preserving aspect ratio."""
    h, w = img.shape[:2]
    if max(h, w) <= max_dim:
        return img
    
    scale = max_dim / float(max(h, w))
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
