import joblib
from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.explainability.shap_explainer import FraudExplainer
from ml_pipeline.config.paths import (
    RANDOM_FOREST_MODEL_PATH,
    PREPROCESSOR_PATH,
)


transaction = {
    "step": 1,
    "type": "TRANSFER",
    "amount": 181.0,
    "oldbalanceOrg": 181.0,
    "newbalanceOrig": 0.0,
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0,
    "isFlaggedFraud": 0,
    "origin_balance_error": 0.0,
    "destination_balance_error": 181.0,
    "origin_balance_change": -181.0,
    "destination_balance_change": 181.0,
}


# Load model and preprocessor
model = joblib.load(
    RANDOM_FOREST_MODEL_PATH
)

preprocessor = FraudPreprocessor.load(
    PREPROCESSOR_PATH
)


# Convert transaction to DataFrame
import pandas as pd

df = pd.DataFrame([transaction])

# Apply same preprocessing
X_processed = preprocessor.transform(df)

# Get exact transformed feature names
feature_names = (
    preprocessor
    .get_feature_names_out()
)


# Explain
explainer = FraudExplainer(
    model=model,
    feature_names=feature_names,
)

explanations = explainer.explain(
    X_processed,
    top_n=10,
)


print("\n" + "=" * 70)
print("FINGUARD AI — SHAP EXPLANATION")
print("=" * 70)

for item in explanations:
    print(
        f"{item['feature']:40} "
        f"value={item['value']:.4f} "
        f"SHAP={item['shap_value']:.6f} "
        f"direction={item['direction']}"
    )