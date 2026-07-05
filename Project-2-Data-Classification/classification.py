"""
classification.py
------------------
Supervised classification of flower species using a K-Nearest Neighbors (KNN)
classifier built with scikit-learn.

Pipeline: Load -> Preprocess -> Scale -> Split -> Train -> Predict -> Evaluate

Author: AI Engineering Portfolio
Python Version: 3.12+
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

DATA_PATH = Path(__file__).parent / "dataset.csv"
CONFUSION_MATRIX_PATH = Path(__file__).parent / "confusion_matrix.png"
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_NEIGHBORS = 5


def load_dataset(filepath: Path) -> pd.DataFrame:
    """Load the classification dataset from a CSV file.

    Args:
        filepath: Path to the CSV dataset.

    Returns:
        A pandas DataFrame containing the raw dataset.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If the dataset is empty.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    dataframe = pd.read_csv(filepath)

    if dataframe.empty:
        raise ValueError("Loaded dataset is empty.")

    return dataframe


def preprocess_data(dataframe: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, LabelEncoder]:
    """Split features/target and encode the categorical target column.

    Args:
        dataframe: Raw input DataFrame with feature columns and a 'species' column.

    Returns:
        A tuple of (feature_matrix, encoded_labels, fitted_label_encoder).
    """
    if "species" not in dataframe.columns:
        raise KeyError("Expected a 'species' column in the dataset.")

    if dataframe.isnull().values.any():
        # Simple, transparent strategy: drop rows with missing values.
        dataframe = dataframe.dropna()

    feature_columns = [col for col in dataframe.columns if col != "species"]
    features = dataframe[feature_columns].to_numpy()

    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(dataframe["species"])

    return features, labels, label_encoder


def scale_features(
    x_train: np.ndarray, x_test: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """Standardize features to zero mean and unit variance.

    KNN is a distance-based algorithm, so feature scaling is essential —
    otherwise features with larger numeric ranges would dominate the
    distance calculation.

    Args:
        x_train: Training feature matrix.
        x_test: Test feature matrix.

    Returns:
        Tuple of (scaled_x_train, scaled_x_test, fitted_scaler).
    """
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    return x_train_scaled, x_test_scaled, scaler


def train_knn(
    x_train: np.ndarray, y_train: np.ndarray, n_neighbors: int = N_NEIGHBORS
) -> KNeighborsClassifier:
    """Train a K-Nearest Neighbors classifier.

    Args:
        x_train: Scaled training feature matrix.
        y_train: Encoded training labels.
        n_neighbors: Number of neighbors (the 'K' in KNN).

    Returns:
        A fitted KNeighborsClassifier.
    """
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(x_train, y_train)
    return model


def evaluate_model(
    model: KNeighborsClassifier,
    x_test: np.ndarray,
    y_test: np.ndarray,
    label_encoder: LabelEncoder,
) -> dict:
    """Evaluate a trained classifier and produce standard metrics.

    Args:
        model: A fitted classifier.
        x_test: Scaled test feature matrix.
        y_test: True encoded test labels.
        label_encoder: The LabelEncoder used to decode class names.

    Returns:
        A dictionary of evaluation metrics and artifacts.
    """
    predictions = model.predict(x_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision_macro": precision_score(y_test, predictions, average="macro"),
        "recall_macro": recall_score(y_test, predictions, average="macro"),
        "f1_macro": f1_score(y_test, predictions, average="macro"),
        "confusion_matrix": confusion_matrix(y_test, predictions),
        "classification_report": classification_report(
            y_test, predictions, target_names=label_encoder.classes_
        ),
        "predictions": predictions,
    }
    return metrics


def plot_confusion_matrix(
    cm: np.ndarray, class_names: np.ndarray, output_path: Path
) -> None:
    """Render and save a confusion matrix heatmap.

    Args:
        cm: Confusion matrix array.
        class_names: Ordered array of class label names.
        output_path: File path where the PNG image will be saved.
    """
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix — KNN Flower Species Classifier")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    """Run the full classification pipeline end-to-end."""
    print("Loading dataset...")
    dataframe = load_dataset(DATA_PATH)
    print(f"Loaded {len(dataframe)} rows, {dataframe.shape[1]} columns.")

    print("Preprocessing data...")
    features, labels, label_encoder = preprocess_data(dataframe)

    print("Splitting into train/test sets...")
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=labels,
    )

    print("Scaling features...")
    x_train_scaled, x_test_scaled, _scaler = scale_features(x_train, x_test)

    print(f"Training KNN classifier (k={N_NEIGHBORS})...")
    model = train_knn(x_train_scaled, y_train)

    print("Evaluating model...")
    metrics = evaluate_model(model, x_test_scaled, y_test, label_encoder)

    print("\n--- Results ---")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision_macro']:.4f}")
    print(f"Recall:    {metrics['recall_macro']:.4f}")
    print(f"F1 Score:  {metrics['f1_macro']:.4f}\n")
    print(metrics["classification_report"])

    plot_confusion_matrix(
        metrics["confusion_matrix"], label_encoder.classes_, CONFUSION_MATRIX_PATH
    )
    print(f"Confusion matrix saved to: {CONFUSION_MATRIX_PATH}")


if __name__ == "__main__":
    main()
