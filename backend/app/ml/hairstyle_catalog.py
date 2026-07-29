from typing import List
from app.models.schemas import HairstyleItem


HAIRSTYLE_CATALOG: List[HairstyleItem] = [
    # --- MASCULINE STYLES ---
    HairstyleItem(
        id="masculine-textured-crop",
        name="Textured Crop",
        presentation="masculine",
        category="Short",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Square"],
        suitable_textures=["Straight", "Wavy"],
        description="A modern short crop with textured volume on top and faded sides.",
        prompt_hint="modern textured crop cut hairstyle, short textured hair on top, neatly tapered sides"
    ),
    HairstyleItem(
        id="masculine-buzz-cut",
        name="Buzz Cut",
        presentation="masculine",
        category="Short",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Square"],
        suitable_textures=["Straight", "Wavy", "Curly", "Coily"],
        description="A clean, minimalist short buzz cut defining strong facial structure.",
        prompt_hint="clean sharp buzz cut hairstyle, uniform short hair"
    ),
    HairstyleItem(
        id="masculine-french-crop",
        name="French Crop",
        presentation="masculine",
        category="Short",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="Short hair with a straight or textured fringe cut across the forehead.",
        prompt_hint="french crop hairstyle with blunt fringe and faded sides"
    ),
    HairstyleItem(
        id="masculine-side-part",
        name="Classic Side Part",
        presentation="masculine",
        category="Short",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Square", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="A classic polished side-part style ideal for both casual and formal looks.",
        prompt_hint="classic neat side part hairstyle, combed elegant finish"
    ),
    HairstyleItem(
        id="masculine-textured-quiff",
        name="Textured Quiff",
        presentation="masculine",
        category="Medium",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Round", "Square"],
        suitable_textures=["Straight", "Wavy"],
        description="Dynamic upward-brushed quiff providing forehead height and texture.",
        prompt_hint="voluminous textured quiff hairstyle, brushed upward and back"
    ),
    HairstyleItem(
        id="masculine-pompadour",
        name="Modern Pompadour",
        presentation="masculine",
        category="Medium",
        maintenance="High",
        suitable_face_shapes=["Oval", "Round"],
        suitable_textures=["Straight", "Wavy"],
        description="Swept back high-volume hairstyle with sleek, tapered sides.",
        prompt_hint="modern high-volume pompadour hairstyle, sleek back wave"
    ),
    HairstyleItem(
        id="masculine-slick-back",
        name="Slick Back",
        presentation="masculine",
        category="Medium",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Square"],
        suitable_textures=["Straight", "Wavy"],
        description="Streamlined slicked-back hairstyle emphasizing jawline geometry.",
        prompt_hint="slicked back hairstyle, smooth clean look"
    ),
    HairstyleItem(
        id="masculine-undercut",
        name="Disconnected Undercut",
        presentation="masculine",
        category="Medium",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Heart", "Square"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="Longer top hair sharply contrasted against shaved or short undercut sides.",
        prompt_hint="disconnected undercut hairstyle, longer voluminous top"
    ),
    HairstyleItem(
        id="masculine-crew-cut",
        name="Classic Crew Cut",
        presentation="masculine",
        category="Short",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Square"],
        suitable_textures=["Straight", "Wavy"],
        description="Timeless short hairstyle slightly longer on top and tapered at sides.",
        prompt_hint="classic crew cut hairstyle, neat short top taper"
    ),
    HairstyleItem(
        id="masculine-low-fade",
        name="Low Fade with Flow",
        presentation="masculine",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Heart", "Square"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="Gentle low fade around ears blending into natural textured top.",
        prompt_hint="low fade hairstyle with natural wavy flow on top"
    ),

    # --- FEMININE STYLES ---
    HairstyleItem(
        id="feminine-long-waves",
        name="Long Layered Waves",
        presentation="feminine",
        category="Long",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Square", "Round", "Heart"],
        suitable_textures=["Wavy", "Curly", "Straight"],
        description="Cascading long layered waves that soften facial angles and add movement.",
        prompt_hint="long lush layered wavy hairstyle cascading down shoulders"
    ),
    HairstyleItem(
        id="feminine-curtain-bangs",
        name="Curtain Bangs & Layers",
        presentation="feminine",
        category="Medium",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Heart", "Round", "Square"],
        suitable_textures=["Straight", "Wavy"],
        description="Face-framing curtain bangs parting gracefully across the forehead.",
        prompt_hint="soft curtain bangs with medium shoulder-length layered hair"
    ),
    HairstyleItem(
        id="feminine-side-bangs",
        name="Side-Swept Bangs",
        presentation="feminine",
        category="Medium",
        maintenance="Medium",
        suitable_face_shapes=["Heart", "Round", "Square", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="Elegant side-swept fringe that visually balances forehead proportions.",
        prompt_hint="chic side-swept fringe bangs with soft hair layers"
    ),
    HairstyleItem(
        id="feminine-butterfly-cut",
        name="Butterfly Cut",
        presentation="feminine",
        category="Long",
        maintenance="High",
        suitable_face_shapes=["Oval", "Square", "Heart"],
        suitable_textures=["Straight", "Wavy"],
        description="Feathered wing-like layers creating multi-dimensional volume.",
        prompt_hint="trendy butterfly cut hairstyle with airy voluminous layered wings"
    ),
    HairstyleItem(
        id="feminine-classic-bob",
        name="Classic French Bob",
        presentation="feminine",
        category="Short",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Heart", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="Chin-length precise cut highlighting cheekbones and neckline.",
        prompt_hint="chic french chin-length bob hairstyle with subtle bend"
    ),
    HairstyleItem(
        id="feminine-lob",
        name="Textured Long Bob (Lob)",
        presentation="feminine",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Square", "Heart", "Oblong"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="Versatile shoulder-grazing cut offering effortless modern elegance.",
        prompt_hint="textured lob cut, shoulder-length wavy bob"
    ),
    HairstyleItem(
        id="feminine-shag",
        name="Modern Layered Shag",
        presentation="feminine",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Square", "Round"],
        suitable_textures=["Wavy", "Curly", "Straight"],
        description="Choppy, piecey layers full of natural texture and movement.",
        prompt_hint="modern shag cut hairstyle with piecey textured fringe"
    ),
    HairstyleItem(
        id="feminine-pixie-cut",
        name="Soft Pixie Cut",
        presentation="feminine",
        category="Short",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Heart", "Square"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="Bold, charming short crop framing eyes and cheekbones.",
        prompt_hint="soft feminine pixie cut hairstyle, delicate textured top"
    ),
    HairstyleItem(
        id="feminine-soft-layers",
        name="Soft Face-Framing Layers",
        presentation="feminine",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Square", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="Gentle cascading layers designed to soften jawline and neck contours.",
        prompt_hint="soft face-framing layered hair cut smoothly falling past shoulders"
    ),
    HairstyleItem(
        id="feminine-long-straight",
        name="Sleek Long Straight Layers",
        presentation="feminine",
        category="Long",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Round", "Square"],
        suitable_textures=["Straight"],
        description="Ultra-smooth, glossy long hair with precise clean ends.",
        prompt_hint="sleek glossy straight long hairstyle with clean blunt ends"
    ),

    # --- UNISEX STYLES ---
    HairstyleItem(
        id="unisex-medium-layered",
        name="Medium Layered Cut",
        presentation="unisex",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Square", "Heart", "Oblong"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="A universally flattering mid-length cut with soft natural movement.",
        prompt_hint="unisex medium layered hair cut with natural soft movement"
    ),
    HairstyleItem(
        id="unisex-wolf-cut",
        name="Modern Wolf Cut",
        presentation="unisex",
        category="Medium",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Round", "Square", "Heart"],
        suitable_textures=["Wavy", "Curly", "Straight"],
        description="Edgy combination of shag and mullet featuring airy face-framing fringe.",
        prompt_hint="trendy wolf cut hairstyle with wild textured layers and curtain fringe"
    ),
    HairstyleItem(
        id="unisex-textured-shag",
        name="Unisex Textured Shag",
        presentation="unisex",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Square", "Oblong"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="Relaxed choppy cut with piecey bang layers for effortless styling.",
        prompt_hint="unisex choppy shag cut with natural waves and soft fringe"
    ),
    HairstyleItem(
        id="unisex-blunt-bob",
        name="Blunt Minimalist Bob",
        presentation="unisex",
        category="Short",
        maintenance="Medium",
        suitable_face_shapes=["Oval", "Heart", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="Sharp architectural chin-length cut emphasizing structural symmetry.",
        prompt_hint="minimalist architectural blunt chin-length bob"
    ),
    HairstyleItem(
        id="unisex-textured-crop",
        name="Universal Textured Crop",
        presentation="unisex",
        category="Short",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Round", "Square", "Heart"],
        suitable_textures=["Straight", "Wavy", "Curly"],
        description="Versatile short crop cut with crown texture and subtle side taper.",
        prompt_hint="universal short textured crop cut with airy fringe"
    ),
    HairstyleItem(
        id="unisex-curtain-fringe",
        name="Curtain Fringe & Flow",
        presentation="unisex",
        category="Medium",
        maintenance="Low",
        suitable_face_shapes=["Oval", "Square", "Heart", "Oblong"],
        suitable_textures=["Straight", "Wavy"],
        description="Center-parted curtain fringe sweeping gracefully into natural mid-length waves.",
        prompt_hint="center-parted curtain fringe hairstyle with effortless natural flow"
    )
]


def get_catalog() -> List[HairstyleItem]:
    return HAIRSTYLE_CATALOG
