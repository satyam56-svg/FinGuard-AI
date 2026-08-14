import joblib

from ml_pipeline.data.data_loader import DataLoader
from ml_pipeline.data.feature_engineering import FeatureEngineer
from ml_pipeline.data.dataset_splitter import DatasetSplitter
from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.evaluation.threshold_analyzer import ThresholdAnalyzer
from ml_pipeline.config.paths import (
    RANDOM_FOREST_MODEL_PATH,
    PREPROCESSOR_PATH,
)


# Load data
df = DataLoader().load()

X, y = FeatureEngineer().transform(df)

# Validation only
_, X_val, _, _, y_val, _ = DatasetSplitter().split(
    X,
    y,
)

# Load fitted preprocessor
preprocessor = FraudPreprocessor.load(
    PREPROCESSOR_PATH
)

X_val_processed = preprocessor.transform(
    X_val
)

# Load champion baseline
model = joblib.load(
    RANDOM_FOREST_MODEL_PATH
)

# Probability of fraud
y_prob = model.predict_proba(
    X_val_processed
)[:, 1]


# Threshold analysis
analyzer = ThresholdAnalyzer()

results = analyzer.analyze(
    y_val,
    y_prob,
)

print("\n" + "=" * 90)
print("RANDOM FOREST — VALIDATION THRESHOLD ANALYSIS")
print("=" * 90)

print(
    results.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}",
    )
)

print("\n" + "=" * 90)
print("BEST F1 THRESHOLD")
print("=" * 90)

best = analyzer.find_best_f1(results)

for key, value in best.items():
    print(f"{key}: {value}")