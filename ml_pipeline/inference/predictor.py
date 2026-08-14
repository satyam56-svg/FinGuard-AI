"""
ml_pipeline/inference/predictor.py

Production inference layer for FinGuard AI.

Combines:
- ML prediction
- Risk Engine
- SHAP explainability
- Human-readable explanation
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from ml_pipeline.config.config import config

import joblib
import pandas as pd

from ml_pipeline.config.paths import (
    RANDOM_FOREST_MODEL_PATH,
    PREPROCESSOR_PATH,
)

from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor
from ml_pipeline.risk.risk_engine import RiskEngine
from ml_pipeline.explainability.shap_explainer import FraudExplainer
from ml_pipeline.explainability.explanation_formatter import (
    ExplanationFormatter,
)


class FraudPredictor:
    """Runs the complete FinGuard AI inference pipeline."""

    def __init__(
        self,
        model_path: str | Path = RANDOM_FOREST_MODEL_PATH,
        preprocessor_path: str | Path = PREPROCESSOR_PATH,
        fraud_threshold: float = config.fraud_threshold,
    ) -> None:

        self.model_path = Path(model_path)
        self.preprocessor_path = Path(preprocessor_path)

        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Model artifact not found: {self.model_path}"
            )

        if not self.preprocessor_path.is_file():
            raise FileNotFoundError(
                f"Preprocessor artifact not found: "
                f"{self.preprocessor_path}"
            )

        self.model = joblib.load(self.model_path)

        self.preprocessor = FraudPreprocessor.load(
            self.preprocessor_path
        )

        self.risk_engine = RiskEngine(
            fraud_threshold=fraud_threshold
        )

        self.explainer = FraudExplainer(
            model=self.model,
            feature_names=self.preprocessor.get_feature_names_out(),
        )

        self.formatter = ExplanationFormatter()

    def predict(
        self,
        transaction: dict[str, Any],
    ) -> dict[str, Any]:
        """Run complete fraud detection and explanation."""

        if not isinstance(transaction, dict):
            raise TypeError(
                "transaction must be a dictionary."
            )

        df = pd.DataFrame([transaction])

        # -----------------------------
        # Preprocessing
        # -----------------------------

        X_processed = self.preprocessor.transform(df)

        # -----------------------------
        # ML Prediction
        # -----------------------------

        fraud_probability = float(
            self.model.predict_proba(
                X_processed
            )[0][1]
        )

        prediction = int(
            fraud_probability
            >= self.risk_engine.fraud_threshold
        )

        # -----------------------------
        # Risk Engine
        # -----------------------------

        risk = self.risk_engine.evaluate(
            fraud_probability
        )

        # -----------------------------
        # SHAP Explanation
        # -----------------------------

        raw_explanations = self.explainer.explain(
            X_processed,
            top_n=10,
        )

        explanation = self.formatter.format(
            raw_explanations,
            top_n=5,
        )

        # -----------------------------
        # Complete Result
        # -----------------------------

        return {
            "prediction": prediction,
            "fraud_probability": round(
                fraud_probability,
                6,
            ),
            "risk_score": risk.risk_score,
            "risk_level": risk.risk_level,
            "recommendation": risk.recommendation,
            "explanation": explanation,
        }