import json
import csv
import os
import numpy as np

"""
Dataset preparation script for AI Hairstyle Advisor ML pipeline.
Generates realistic geometric feature distributions for facial landmark ratios:
- Oval: Balanced length/width ratio (1.30 - 1.40), soft jaw taper
- Round: Near 1:1 length/width ratio (1.00 - 1.15), rounded cheekbones
- Square: Wide jaw matching cheekbone width (aspect ratio 1.05 - 1.20)
- Heart: Wide forehead, sharply tapering narrow jaw
- Oblong: Visually elongated face (aspect ratio 1.42 - 1.60)
"""

DATASET_SCHEMA = [
    "image_id",
    "face_length",
    "face_width",
    "forehead_width",
    "cheekbone_width",
    "jaw_width",
    "aspect_ratio",
    "hair_length",
    "hair_texture",
    "hair_density",
    "style_preference",
    "face_shape_label",
    "target_hairstyle_id",
    "suitability_rating"
]


def generate_geometric_dataset(output_csv: str = "dataset.csv", num_samples: int = 1000):
    shapes = ["Oval", "Round", "Square", "Heart", "Oblong"]
    textures = ["Straight", "Wavy", "Curly", "Coily"]
    lengths = ["Short", "Medium", "Long"]
    preferences = ["masculine", "feminine", "unisex", "no_preference"]
    hairstyles = ["textured-crop", "long-waves", "curtain-bangs", "buzz-cut", "wolf-cut", "french-bob"]

    np.random.seed(42)
    os.makedirs(os.path.dirname(output_csv) if os.path.dirname(output_csv) else ".", exist_ok=True)

    with open(output_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(DATASET_SCHEMA)

        for i in range(num_samples):
            shape = np.random.choice(shapes)
            cheek = np.random.uniform(160, 200)

            if shape == "Oval":
                aspect = np.random.uniform(1.30, 1.40)
                forehead = cheek * np.random.uniform(0.82, 0.88)
                jaw = cheek * np.random.uniform(0.74, 0.80)
            elif shape == "Round":
                aspect = np.random.uniform(1.02, 1.15)
                forehead = cheek * np.random.uniform(0.85, 0.92)
                jaw = cheek * np.random.uniform(0.80, 0.88)
            elif shape == "Square":
                aspect = np.random.uniform(1.08, 1.22)
                forehead = cheek * np.random.uniform(0.92, 0.98)
                jaw = cheek * np.random.uniform(0.92, 0.98)
            elif shape == "Heart":
                aspect = np.random.uniform(1.22, 1.35)
                forehead = cheek * np.random.uniform(0.95, 1.05)
                jaw = cheek * np.random.uniform(0.60, 0.70)
            elif shape == "Oblong":
                aspect = np.random.uniform(1.42, 1.60)
                forehead = cheek * np.random.uniform(0.80, 0.88)
                jaw = cheek * np.random.uniform(0.75, 0.85)

            face_length = cheek * aspect
            face_width = cheek

            row = [
                f"img_{i:05d}",
                round(face_length, 1),
                round(face_width, 1),
                round(forehead, 1),
                round(cheek, 1),
                round(jaw, 1),
                round(aspect, 2),
                np.random.choice(lengths),
                np.random.choice(textures),
                "Medium",
                np.random.choice(preferences),
                shape,
                np.random.choice(hairstyles),
                round(np.random.uniform(4.0, 5.0), 1)
            ]
            writer.writerow(row)

    print(f"Realistic facial landmark dataset preparation complete: {output_csv} created with {num_samples} records.")


if __name__ == "__main__":
    generate_geometric_dataset()
