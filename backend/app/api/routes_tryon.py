from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.models.schemas import TryOnResponse
from app.services.virtual_tryon import get_virtual_tryon_provider
from app.utils.image_utils import decode_image_bytes

router = APIRouter(prefix="/api", tags=["Virtual Try-On"])


@router.post("/try-on", response_model=TryOnResponse)
async def try_on_hairstyle(
    file: UploadFile = File(...),
    hairstyle_name: str = Form(...),
    prompt_hint: str = Form("")
):
    """
    Generates photorealistic AI Virtual Try-On image preview of selected hairstyle on uploaded photo.
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image file is required for virtual try-on."
        )

    content = await file.read()
    try:
        img_bgr = decode_image_bytes(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file: {str(e)}"
        )

    try:
        provider = get_virtual_tryon_provider()
        tryon_url = provider.generate(img_bgr, hairstyle_name=hairstyle_name, prompt_hint=prompt_hint)

        return TryOnResponse(
            success=True,
            tryon_image_url=tryon_url,
            message="Virtual try-on preview generated successfully.",
            hairstyle_name=hairstyle_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Virtual try-on generation failed: {str(e)}"
        )
