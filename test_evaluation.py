"""
FinGuard AI — Final Baseline Test Evaluation

Evaluates all five trained baseline models on the untouched
test set using the same fitted preprocessing artifact.
"""

from __future__ import annotations

import joblib
import pandas as pd

from ml_pipeline.data.data_loader import DataLoader
from ml_pipeline.data.feature_engineering import FeatureEngineer
from ml_pipeline.data.dataset_splitter import DatasetSplitter
from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.evaluation.evaluator import ModelEvaluator
from ml_pipeline.config.paths import MODEL_PATHS, PREPROCESSOR_PATH


# ---------------------------------------------------------
# Load data and recreate deterministic split
# ---------------------------------------------------------

print("Loading dataset...")

df = DataLoader().load()

X, y = FeatureEngineer().transform(df)

_, _, X_test, _, _, y_test = DatasetSplitter().split(
    X,
    y,
)

print(f"Test samples: {len(X_test)}")
print(f"Test fraud cases: {int(y_test.sum())}")


# ---------------------------------------------------------
# Load fitted preprocessor
# ---------------------------------------------------------

preprocessor = FraudPreprocessor.load(
    PREPROCESSOR_PATH
)

X_test_processed = preprocessor.transform(X_test)


# ---------------------------------------------------------
# Evaluate all models
# ---------------------------------------------------------

evaluator = ModelEvaluator()

results = []


for model_key, model_path in MODEL_PATHS.items():

    model_name = model_key.replace(
        "_",
        " ",
    ).title()

    print(f"\nEvaluating {model_name}...")

    model = joblib.load(model_path)

    result = evaluator.evaluate(
        model,
        X_test_processed,
        y_test,
    )

    cm = result["confusion_matrix"]

    results.append(
        {
            "Model": model_name,
            "Accuracy": result["accuracy"],
            "Precision": result["precision"],
            "Recall": result["recall"],
            "F1": result["f1"],
            "ROC-AUC": result["roc_auc"],
            "PR-AUC": result["pr_auc"],
            "False Positives": cm["false_positives"],
            "False Negatives": cm["false_negatives"],
        }
    )


# ---------------------------------------------------------
# Final comparison
# ---------------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1",
    ascending=False,
)


print("\n" + "=" * 100)
print("FINAL BASELINE TEST EVALUATION")
print("=" * 100)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}",
    )
)