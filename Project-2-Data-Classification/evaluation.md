# Evaluation — Confusion Matrix & Metrics Explained

## Confusion Matrix

The confusion matrix (`confusion_matrix.png`) is a 3×3 grid (one row/column
per species: `setosa`, `versicolor`, `virginica`) where:

- **Rows** represent the true (actual) class.
- **Columns** represent the predicted class.
- **Diagonal cells** are correct predictions.
- **Off-diagonal cells** are misclassifications.

For this run (test set of 30 samples, 10 per class):

```
                Predicted
              set  ver  vir
True   set  [ 10    0    0 ]
       ver  [  0   10    0 ]
       vir  [  0    2    8 ]
```

Interpretation: all `setosa` and `versicolor` samples were classified
correctly. 2 `virginica` samples were misclassified as `versicolor` — this
is expected, since `versicolor` and `virginica` have overlapping petal
measurement ranges in the dataset, making them the hardest pair to separate
linearly.

## Metric Definitions

| Metric | Formula | Meaning |
|---|---|---|
| **Accuracy** | (TP + TN) / Total | Overall fraction of correct predictions across all classes |
| **Precision** (macro) | Average of TP / (TP + FP) per class | Of all predicted-as-class-X, how many were actually class X |
| **Recall** (macro) | Average of TP / (TP + FN) per class | Of all actual class-X, how many were correctly identified |
| **F1 Score** (macro) | 2 × (Precision × Recall) / (Precision + Recall) | Harmonic mean balancing precision and recall |

We use **macro averaging** (simple average across the 3 classes) rather than
weighted/micro averaging because the dataset is balanced (50 samples per
class), so each class should contribute equally to the overall score.

## Why Not Just Use Accuracy?

Accuracy alone can be misleading on imbalanced datasets — a classifier that
always predicts the majority class can achieve high accuracy while being
useless for minority classes. Precision, recall, and F1 give a fuller picture
per class, which is why `classification_report()` breaks metrics down by
class in addition to the overall macro average.

## Common Misclassification Patterns

`versicolor` and `virginica` are the two species most often confused because
their petal length/width ranges overlap (see `dataset.csv` generation
ranges). `setosa` is linearly separable from the other two and is rarely, if
ever, misclassified — this is a well-known property of this style of flower
classification dataset.
