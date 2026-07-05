# Model Training — Data Classification

## Algorithm: K-Nearest Neighbors (KNN)

KNN is a non-parametric, instance-based classification algorithm. To
classify a new sample, it:

1. Computes the distance (Euclidean by default) between the new sample and every training sample.
2. Selects the `K` nearest training samples.
3. Assigns the majority class among those `K` neighbors as the prediction.

We use `K = 5` (`N_NEIGHBORS = 5` in `classification.py`).

## Pipeline Stages

### 1. Load Dataset
`load_dataset()` reads `dataset.csv` with pandas, validating the file exists and is non-empty.

### 2. Preprocessing
`preprocess_data()`:
- Drops rows containing missing values.
- Separates feature columns (`sepal_length`, `sepal_width`, `petal_length`, `petal_width`) from the target column (`species`).
- Encodes the categorical `species` labels into integers using `LabelEncoder` (`setosa=0`, `versicolor=1`, `virginica=2` after fitting).

### 3. Train/Test Split
`train_test_split()` from scikit-learn reserves 20% of the data for testing
(`TEST_SIZE = 0.2`), with `stratify=labels` ensuring class proportions are
preserved in both splits, and `random_state=42` for reproducibility.

### 4. Feature Scaling
`scale_features()` applies `StandardScaler`, transforming each feature to
zero mean and unit variance. This step is **critical for KNN** because it is
a distance-based algorithm — without scaling, a feature measured in larger
units would disproportionately dominate the Euclidean distance calculation.

> Important: the scaler is `fit` only on the training data and then used to
> `transform` the test data, preventing data leakage from the test set into
> the scaling parameters.

### 5. Model Training
`train_knn()` instantiates `KNeighborsClassifier(n_neighbors=5)` and calls
`.fit(x_train, y_train)`.

### 6. Prediction & Evaluation
`evaluate_model()` calls `.predict()` on the scaled test set and computes
accuracy, macro-averaged precision/recall/F1, the confusion matrix, and a
full `classification_report`.

## Choosing K

| K | Effect |
|---|---|
| Too small (e.g., 1) | Overfits — sensitive to noise/outliers |
| Too large | Underfits — decision boundary becomes overly smooth, may ignore local structure |
| K = 5 (chosen) | Good general-purpose default for small, balanced datasets |

In production, `K` should be tuned via cross-validation (e.g.
`GridSearchCV` over `n_neighbors=[1,3,5,7,9,11]`).

## Reproducibility

`RANDOM_STATE = 42` is used consistently for the train/test split, ensuring
the same split — and therefore the same reported metrics — every time the
script is run on the same dataset.
