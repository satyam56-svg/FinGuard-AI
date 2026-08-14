import joblib
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

from ml_pipeline.data.data_loader import DataLoader
from ml_pipeline.data.feature_engineering import FeatureEngineer
from ml_pipeline.data.dataset_splitter import DatasetSplitter
from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.config.paths import (
    RANDOM_FOREST_MODEL_PATH,
    PREPROCESSOR_PATH,
)


# ---------------------------------------------------------
# Load dataset and recreate deterministic split
# ---------------------------------------------------------

df = DataLoader().load()

X, y = FeatureEngineer().transform(df)

_, _, X_test, _, _, y_test = DatasetSplitter().split(
    X,
    y,
)

print("Test samples:", len(X_test))
print("Test fraud cases:", int(y_test.sum()))


# ---------------------------------------------------------
# Load saved artifacts
# ---------------------------------------------------------

preprocessor = FraudPreprocessor.load(
    PREPROCESSOR_PATH
)

model = joblib.load(
    RANDOM_FOREST_MODEL_PATH
)

X_test_processed = preprocessor.transform(
    X_test
)


# ---------------------------------------------------------
# Get fraud probabilities
# ---------------------------------------------------------

y_prob = model.predict_proba(
    X_test_processed
)[:, 1]


# ---------------------------------------------------------
# Evaluate candidate thresholds
# ---------------------------------------------------------

thresholds = [
    0.50,
    0.60,
    0.70,
    0.80,
]

results = []

for threshold in thresholds:

    y_pred = (
        y_prob >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    false_positives = int(
        ((y_test == 0) & (y_pred == 1)).sum()
    )

    false_negatives = int(
        ((y_test == 1) & (y_pred == 0)).sum()
    )

    results.append(
        {
            "threshold": threshold,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
        }
    )


results_df = pd.DataFrame(results)


print("\n" + "=" * 90)
print("RANDOM FOREST — TEST THRESHOLD ANALYSIS")
print("=" * 90)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}",
    )
)