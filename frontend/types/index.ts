export type StylePreferenceType = 'masculine' | 'feminine' | 'unisex' | 'no_preference';

export interface FaceMeasurements {
  face_length: number;
  face_width: number;
  forehead_width: number;
  cheekbone_width: number;
  jaw_width: number;
  aspect_ratio: number;
}

export interface FaceAnalysisResult {
  face_detected: boolean;
  face_count: number;
  face_shape?: string;
  confidence?: number;
  measurements?: FaceMeasurements;
  error?: string;
  disclaimer?: string;
}

export interface HairCharacteristics {
  hair_length: string;
  hair_texture: string;
  hair_density: string;
  hair_volume: string;
}

export interface HairstyleItem {
  id: string;
  name: string;
  presentation: 'masculine' | 'feminine' | 'unisex';
  category: 'Short' | 'Medium' | 'Long';
  maintenance: 'Low' | 'Medium' | 'High';
  suitable_face_shapes: string[];
  suitable_textures: string[];
  description: string;
  prompt_hint?: string;
}

export interface RecommendationItem {
  hairstyle: HairstyleItem;
  name: string;
  match_score: number;
  reason: string;
}

export interface RecommendationResponse {
  recommendations: RecommendationItem[];
  total: number;
}

export interface TryOnResponse {
  success: boolean;
  tryon_image_url: string;
  message: string;
  hairstyle_name: string;
}
