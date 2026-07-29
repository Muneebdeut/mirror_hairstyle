import io
import base64
import numpy as np
from PIL import Image
from typing import Tuple

try:
    import cv2
except ImportError:
    cv2 = None


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decode raw image bytes into an RGB/BGR image numpy array."""
    if cv2 is not None:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            return img

    # PIL fallback
    img_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return np.array(img_pil)


def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """Convert BGR image to RGB."""
    if cv2 is not None and isinstance(img_bgr, np.ndarray) and len(img_bgr.shape) == 3 and img_bgr.shape[2] == 3:
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_bgr


def encode_image_to_base64_data_url(img_arr: np.ndarray, format_ext: str = ".jpg") -> str:
    """Encode image numpy array to base64 data URL string."""
    if cv2 is not None:
        success, buffer = cv2.imencode(format_ext, img_arr)
        if success:
            b64_str = base64.b64encode(buffer).decode("utf-8")
            mime_type = "image/jpeg" if format_ext.lower() in [".jpg", ".jpeg"] else "image/png"
            return f"data:{mime_type};base64,{b64_str}"

    # PIL fallback
    img_pil = Image.fromarray(img_arr)
    buffer = io.BytesIO()
    fmt = "JPEG" if format_ext.lower() in [".jpg", ".jpeg"] else "PNG"
    img_pil.save(buffer, format=fmt)
    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    mime_type = f"image/{fmt.lower()}"
    return f"data:{mime_type};base64,{b64_str}"


def resize_image_max_dim(img: np.ndarray, max_dim: int = 1024) -> np.ndarray:
    """Resize image so its maximum dimension does not exceed max_dim while preserving aspect ratio."""
    h, w = img.shape[:2]
    if max(h, w) <= max_dim:
        return img
    
    if cv2 is not None:
        scale = max_dim / float(max(h, w))
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # PIL fallback
    img_pil = Image.fromarray(img)
    img_pil.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    return np.array(img_pil)
