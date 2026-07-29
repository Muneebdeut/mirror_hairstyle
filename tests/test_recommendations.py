import pytest
from app.ml.hairstyle_recommender import HairstyleRecommender
from app.models.schemas import RecommendationRequest, StylePreference


def test_recommendations_top_5():
    recommender = HairstyleRecommender()
    req = RecommendationRequest(
        face_shape="Round",
        hairstyle_preference=StylePreference.NO_PREFERENCE,
        hair_length="Medium",
        hair_texture="Wavy"
    )
    res = recommender.recommend(req, limit=5)
    assert len(res.recommendations) == 5
    assert res.total == 5
    assert res.recommendations[0].match_score >= res.recommendations[1].match_score


def test_masculine_preference_ranking():
    recommender = HairstyleRecommender()
    req = RecommendationRequest(
        face_shape="Square",
        hairstyle_preference=StylePreference.MASCULINE
    )
    res = recommender.recommend(req, limit=5)
    # Ensure masculine / unisex styles are prioritized
    top_styles = [item.hairstyle.presentation for item in res.recommendations]
    assert "masculine" in top_styles or "unisex" in top_styles


def test_feminine_preference_ranking():
    recommender = HairstyleRecommender()
    req = RecommendationRequest(
        face_shape="Oval",
        hairstyle_preference=StylePreference.FEMININE
    )
    res = recommender.recommend(req, limit=5)
    top_styles = [item.hairstyle.presentation for item in res.recommendations]
    assert "feminine" in top_styles or "unisex" in top_styles
