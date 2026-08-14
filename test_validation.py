from ml_pipeline.data.data_loader import DataLoader
from ml_pipeline.data.feature_engineering import FeatureEngineer
from ml_pipeline.data.dataset_splitter import DatasetSplitter
from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.evaluation.evaluator import ModelEvaluator
from ml_pipeline.config.paths import MODEL_PATHS

import joblib


# Load dataset
df = DataLoader().load()

# Feature engineering
X, y = FeatureEngineer().transform(df)

# Recreate the same deterministic split
_, X_val, _, _, y_val, _ = DatasetSplitter().split(X, y)

# Load fitted preprocessing pipeline
preprocessor = FraudPreprocessor.load(
    "ml_pipeline/models/preprocessor.pkl"
)

# Load trained LightGBM model
model = joblib.load(
    MODEL_PATHS["lightgbm"]
)

# Transform validation data
X_val_processed = preprocessor.transform(X_val)

# Evaluate
evaluator = ModelEvaluator()

result = evaluator.evaluate(
    model,
    X_val_processed,
    y_val,
)

print("\n" + "=" * 60)
print("LIGHTGBM — VALIDATION")
print("=" * 60)

print(f"Accuracy : {result['accuracy']:.6f}")
print(f"Precision: {result['precision']:.6f}")
print(f"Recall   : {result['recall']:.6f}")
print(f"F1       : {result['f1']:.6f}")
print(f"ROC-AUC  : {result['roc_auc']:.6f}")
print(f"PR-AUC   : {result['pr_auc']:.6f}")

print("\nConfusion Matrix:")
print(result["confusion_matrix"])