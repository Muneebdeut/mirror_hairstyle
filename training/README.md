# Machine Learning Pipeline & Future Roadmap

This directory contains the machine learning training pipeline and dataset formatting scripts for transitioning from rule-based heuristic modules to custom trained deep neural network models.

## Future Dataset Schema

Each training record contains:

```csv
image_id, face_length, face_width, forehead_width, cheekbone_width, jaw_width, aspect_ratio, hair_length, hair_texture, hair_density, style_preference, face_shape_label, target_hairstyle_id, suitability_rating
```

## Future ML Model Architecture

The target recommendation model estimates the conditional probability:

$$P(\text{hairstyle suitability} \mid \text{face shape}, \text{hair characteristics}, \text{hairstyle preference}, \text{user feedback})$$

### Scripts Included

- `prepare_dataset.py`: Converts facial landmark vectors and preference surveys into structured training CSV format.
- `train_face_shape_model.py`: Trains an MLP classifier for facial landmark-based shape estimation.
- `train_recommendation_model.py`: Trains a Neural Collaborative Filtering recommendation network.
- `evaluate_model.py`: Calculates classification precision, recall, F1, and NDCG@5 metrics.
