import joblib
import pandas as pd

from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.explainability.shap_explainer import FraudExplainer
from ml_pipeline.explainability.explanation_formatter import ExplanationFormatter
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


model = joblib.load(
    RANDOM_FOREST_MODEL_PATH
)

preprocessor = FraudPreprocessor.load(
    PREPROCESSOR_PATH
)

df = pd.DataFrame([transaction])

X_processed = preprocessor.transform(df)

explainer = FraudExplainer(
    model=model,
    feature_names=preprocessor.get_feature_names_out(),
)

raw_explanations = explainer.explain(
    X_processed,
    top_n=10,
)

formatter = ExplanationFormatter()

formatted = formatter.format(
    raw_explanations,
    top_n=5,
)

print("\n" + "=" * 70)
print("FINGUARD AI — HUMAN READABLE EXPLANATION")
print("=" * 70)

print("\nRisk Factors:")

for item in formatted["risk_factors"]:
    print(
        f"- {item['feature']} | "
        f"impact={item['impact']:.6f}"
    )

print("\nProtective Factors:")

for item in formatted["protective_factors"]:
    print(
        f"- {item['feature']} | "
        f"impact={item['impact']:.6f}"
    )