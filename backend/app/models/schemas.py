from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class StylePreference(str, Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    UNISEX = "unisex"
    NO_PREFERENCE = "no_preference"


class FaceMeasurements(BaseModel):
    face_length: float = Field(..., description="Vertical distance from forehead to chin in pixels")
    face_width: float = Field(..., description="Maximum horizontal width of the face in pixels")
    forehead_width: float = Field(..., description="Width across the upper forehead in pixels")
    cheekbone_width: float = Field(..., description="Width across the cheekbones in pixels")
    jaw_width: float = Field(..., description="Width across the jawline in pixels")
    aspect_ratio: float = Field(..., description="Ratio of face length to face width")


class FaceAnalysisResponse(BaseModel):
    face_detected: bool
    face_count: int
    face_shape: Optional[str] = None
    confidence: Optional[float] = None
    measurements: Optional[FaceMeasurements] = None
    error: Optional[str] = None
    disclaimer: str = "Face shape is an AI-based estimate and may not be perfectly accurate."


class HairCharacteristics(BaseModel):
    hair_length: str = Field("Unknown", description="Very Short, Short, Medium, Long, Unknown")
    hair_texture: str = Field("Unknown", description="Straight, Wavy, Curly, Coily, Unknown")
    hair_density: str = Field("Unknown", description="Low, Medium, High, Unknown")
    hair_volume: str = Field("Unknown", description="Low, Medium, High, Unknown")


class HairAnalysisResponse(BaseModel):
    hair_characteristics: HairCharacteristics
    confidence: float = 0.85
    message: Optional[str] = None


class RecommendationRequest(BaseModel):
    face_shape: str = Field(..., description="Estimated or user-selected face shape")
    hairstyle_preference: StylePreference = Field(
        StylePreference.NO_PREFERENCE,
        description="Preferred hairstyle presentation filter: masculine, feminine, unisex, no_preference"
    )
    hair_length: Optional[str] = "Medium"
    hair_texture: Optional[str] = "Wavy"
    hair_density: Optional[str] = "Medium"
    maintenance_preference: Optional[str] = "Any"


class HairstyleItem(BaseModel):
    id: str
    name: str
    presentation: str  # masculine, feminine, unisex
    category: str  # Short, Medium, Long
    maintenance: str  # Low, Medium, High
    suitable_face_shapes: List[str]
    suitable_textures: List[str]
    description: str
    prompt_hint: Optional[str] = None


class RecommendationItem(BaseModel):
    hairstyle: HairstyleItem
    name: str
    match_score: int
    reason: str


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    total: int


class TryOnResponse(BaseModel):
    success: bool
    tryon_image_url: str
    message: str
    hairstyle_name: str


class ErrorResponse(BaseModel):
    detail: str
    code: str = "BAD_REQUEST"
