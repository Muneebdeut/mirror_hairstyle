from typing import List, Dict, Any, Optional
from app.models.schemas import (
    RecommendationRequest,
    RecommendationItem,
    RecommendationResponse,
    HairstyleItem,
    StylePreference
)
from app.ml.hairstyle_catalog import get_catalog


class HairstyleRecommender:
    """
    Weighted Hairstyle Recommendation Engine.
    Configurable weights:
    - Face Shape Compatibility: 45%
    - Hairstyle Preference Alignment: 25%
    - Hair Characteristics Compatibility: 15%
    - Maintenance / Style Fit: 15%
    
    Ranks top hairstyles, providing tailored reasoning explanations for each recommendation.
    Can be seamlessly upgraded to a trained Collaborative / Content ML Model.
    """
    
    def __init__(
        self,
        weight_face_shape: float = 0.45,
        weight_preference: float = 0.25,
        weight_hair_traits: float = 0.15,
        weight_maintenance: float = 0.15
    ):
        self.w_face = weight_face_shape
        self.w_pref = weight_preference
        self.w_hair = weight_hair_traits
        self.w_maint = weight_maintenance
        self.catalog = get_catalog()

    def recommend(self, req: RecommendationRequest, limit: int = 5) -> RecommendationResponse:
        scored_items: List[RecommendationItem] = []

        face_shape = req.face_shape.strip().capitalize() if req.face_shape else "Oval"
        pref = req.hairstyle_preference or StylePreference.NO_PREFERENCE
        hair_texture = req.hair_texture or "Wavy"
        hair_length = req.hair_length or "Medium"
        maint_pref = req.maintenance_preference or "Any"

        for style in self.catalog:
            # 1. Face Shape Score (0.0 to 1.0)
            if face_shape in style.suitable_face_shapes:
                face_score = 1.0
            elif "Oval" in style.suitable_face_shapes:
                face_score = 0.70
            else:
                face_score = 0.50

            # 2. Preference Score (0.0 to 1.0)
            if pref == StylePreference.NO_PREFERENCE:
                pref_score = 1.0
            elif pref == StylePreference.MASCULINE:
                if style.presentation == "masculine":
                    pref_score = 1.0
                elif style.presentation == "unisex":
                    pref_score = 0.85
                else:
                    pref_score = 0.40
            elif pref == StylePreference.FEMININE:
                if style.presentation == "feminine":
                    pref_score = 1.0
                elif style.presentation == "unisex":
                    pref_score = 0.85
                else:
                    pref_score = 0.40
            elif pref == StylePreference.UNISEX:
                if style.presentation == "unisex":
                    pref_score = 1.0
                else:
                    pref_score = 0.60
            else:
                pref_score = 0.90

            # 3. Hair Characteristics Score (0.0 to 1.0)
            hair_score = 0.0
            if hair_texture in style.suitable_textures or "Unknown" in style.suitable_textures:
                hair_score += 0.60
            else:
                hair_score += 0.30

            if style.category.lower() == hair_length.lower():
                hair_score += 0.40
            else:
                hair_score += 0.20
            hair_score = min(1.0, hair_score)

            # 4. Maintenance Score (0.0 to 1.0)
            if maint_pref.lower() == "any" or maint_pref.lower() == style.maintenance.lower():
                maint_score = 1.0
            elif maint_pref.lower() == "low" and style.maintenance.lower() == "medium":
                maint_score = 0.75
            else:
                maint_score = 0.60

            # Total Weighted Match Score (percentage 50 to 99)
            total_raw = (
                (face_score * self.w_face) +
                (pref_score * self.w_pref) +
                (hair_score * self.w_hair) +
                (maint_score * self.w_maint)
            )

            # Map total_raw (0.4 to 1.0) to match score (65 to 98)
            match_score = int(round(65 + (total_raw * 33)))
            match_score = max(65, min(98, match_score))

            # Reason generation
            reason = self._generate_reason(style, face_shape, pref, hair_texture)

            scored_items.append(
                RecommendationItem(
                    hairstyle=style,
                    name=style.name,
                    match_score=match_score,
                    reason=reason
                )
            )

        # Sort by match_score descending
        scored_items.sort(key=lambda x: x.match_score, reverse=True)
        top_recommendations = scored_items[:limit]

        return RecommendationResponse(
            recommendations=top_recommendations,
            total=len(top_recommendations)
        )

    def _generate_reason(
        self,
        style: HairstyleItem,
        face_shape: str,
        pref: StylePreference,
        texture: str
    ) -> str:
        shape_reasons = {
            "Oval": "Complements balanced oval facial proportions seamlessly.",
            "Round": "Adds vertical texture and height to visually elongate a round face shape.",
            "Square": "Softens jawline angles with layered texture and organic flow.",
            "Heart": "Balances forehead width and jaw proportions with face-framing softness.",
            "Oblong": "Adds lateral volume and fringe framing to complement face length."
        }
        shape_text = shape_reasons.get(face_shape, "Flatters your face shape and proportions.")
        
        pref_text = ""
        if pref != StylePreference.NO_PREFERENCE:
            pref_text = f" Matches your preferred {pref.value} hairstyle aesthetic."

        return f"{shape_text}{pref_text} Ideal for {texture.lower()} hair texture with {style.maintenance.lower()} maintenance."
