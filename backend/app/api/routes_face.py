from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models.schemas import FaceAnalysisResponse, HairAnalysisResponse
from app.services.face_analysis import FaceAnalysisService
from app.services.hair_analysis import HairAnalysisService
from app.utils.image_utils import decode_image_bytes

router = APIRouter(prefix="/api", tags=["Face & Hair Analysis"])

face_service = FaceAnalysisService()
hair_service = HairAnalysisService()

ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit


@router.post("/analyze-face", response_model=FaceAnalysisResponse)
async def analyze_face(file: UploadFile = File(...)):
    """
    Accepts an uploaded image file (JPG, PNG).
    Validates single face requirement, extracts 3D facial landmarks,
    calculates facial geometry ratios, and returns estimated face shape.
    """
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a JPG, JPEG, or PNG image."
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum file size is 10 MB."
        )

    try:
        img_bgr = decode_image_bytes(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted image file: {str(e)}"
        )

    analysis_res = face_service.analyze_face(img_bgr)
    return analysis_res


@router.post("/analyze-hair", response_model=HairAnalysisResponse)
async def analyze_hair(file: UploadFile = File(...)):
    """
    Analyzes hair region characteristics (length, texture, density) from uploaded image.
    """
    content = await file.read()
    try:
        img_bgr = decode_image_bytes(content)
        return hair_service.analyze_hair(img_bgr)
    except Exception:
        return hair_service.analyze_hair(None)
