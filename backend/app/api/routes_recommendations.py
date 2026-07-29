from fastapi import APIRouter
from app.models.schemas import RecommendationRequest, RecommendationResponse
from app.ml.hairstyle_recommender import HairstyleRecommender

router = APIRouter(prefix="/api", tags=["Hairstyle Recommendations"])
recommender = HairstyleRecommender()


@router.post("/recommend-hairstyles", response_model=RecommendationResponse)
async def recommend_hairstyles(req: RecommendationRequest):
    """
    Ranks top hairstyles using face shape, style preference (masculine, feminine, unisex, no_preference),
    hair characteristics, and maintenance levels.
    """
    return recommender.recommend(req, limit=5)
