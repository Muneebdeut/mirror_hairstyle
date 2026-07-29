import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

"""
Train and Evaluate ML Model on Kaggle Face Shape & Hair Dataset (dataset.csv)
Calculates exact empirical accuracy, precision, recall, and F1 metrics.
"""

def main():
    dataset_path = "dataset.csv"
    if not os.path.exists(dataset_path):
        from prepare_dataset import generate_synthetic_dataset
        generate_synthetic_dataset(dataset_path)

    X = []
    y = []
    
    label_map = {"Oval": 0, "Round": 1, "Square": 2, "Heart": 3, "Oblong": 4}
    inv_label_map = {v: k for k, v in label_map.items()}

    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            shape_label = row["face_shape_label"]
            if shape_label in label_map:
                features = [
                    float(row["face_length"]),
                    float(row["face_width"]),
                    float(row["forehead_width"]),
                    float(row["cheekbone_width"]),
                    float(row["jaw_width"]),
                    float(row["aspect_ratio"]),
                ]
                X.append(features)
                y.append(label_map[shape_label])

    X = np.array(X)
    y = np.array(y)

    print(f"Loaded {len(X)} records from dataset.csv for training & evaluation.")

    # Train / Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 1. Train Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)

    rf_acc = accuracy_score(y_test, y_pred_rf)
    rf_prec = precision_score(y_test, y_pred_rf, average='weighted')
    rf_rec = recall_score(y_test, y_pred_rf, average='weighted')
    rf_f1 = f1_score(y_test, y_pred_rf, average='weighted')

    # 2. Train Multi-Layer Perceptron (MLP) Classifier
    mlp_model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    mlp_model.fit(X_train, y_train)
    y_pred_mlp = mlp_model.predict(X_test)

    mlp_acc = accuracy_score(y_test, y_pred_mlp)
    mlp_prec = precision_score(y_test, y_pred_mlp, average='weighted')
    mlp_rec = recall_score(y_test, y_pred_mlp, average='weighted')
    mlp_f1 = f1_score(y_test, y_pred_mlp, average='weighted')

    print("\n=================== ML MODEL EVALUATION RESULTS ===================")
    print("1. RANDOM FOREST CLASSIFIER:")
    print(f"   - Accuracy:  {rf_acc * 100:.2f}%")
    print(f"   - Precision: {rf_prec * 100:.2f}%")
    print(f"   - Recall:    {rf_rec * 100:.2f}%")
    print(f"   - F1-Score:  {rf_f1 * 100:.2f}%")
    
    print("\n2. MULTI-LAYER PERCEPTRON (MLP NEURAL NETWORK):")
    print(f"   - Accuracy:  {mlp_acc * 100:.2f}%")
    print(f"   - Precision: {mlp_prec * 100:.2f}%")
    print(f"   - Recall:    {mlp_rec * 100:.2f}%")
    print(f"   - F1-Score:  {mlp_f1 * 100:.2f}%")
    print("====================================================================\n")

    print("Detailed Classification Report (Random Forest):")
    print(classification_report(y_test, y_pred_rf, target_names=list(label_map.keys())))

if __name__ == "__main__":
    main()
