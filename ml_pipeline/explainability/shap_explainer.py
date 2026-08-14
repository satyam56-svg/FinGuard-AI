"""
ml_pipeline/explainability/shap_explainer.py

SHAP-based explainability for the FinGuard AI fraud model.

Explains why the trained model produced a particular
fraud probability for a transaction.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import shap


class FraudExplainer:
    """Generate SHAP explanations for a trained fraud model."""

    def __init__(
        self,
        model: Any,
        feature_names: list[str],
    ) -> None:

        if model is None:
            raise ValueError("model cannot be None.")

        if not feature_names:
            raise ValueError(
                "feature_names cannot be empty."
            )

        self.model = model
        self.feature_names = feature_names

        self.explainer = shap.TreeExplainer(
            self.model
        )

    def explain(
        self,
        X: Any,
        top_n: int = 10,
    ) -> list[dict[str, Any]]:

        if X is None:
            raise ValueError("X cannot be None.")

        if X.shape[0] != 1:
            raise ValueError(
                "FraudExplainer.explain() expects "
                "exactly one transaction."
            )

        if X.shape[1] != len(self.feature_names):
            raise ValueError(
                "Number of features does not match "
                "feature_names."
            )

        if top_n <= 0:
            raise ValueError(
                "top_n must be greater than zero."
            )

        shap_values = self.explainer.shap_values(X)

        # SHAP output differs across SHAP versions/models.
        if isinstance(shap_values, list):
            values = np.asarray(
                shap_values[-1]
            )[0]
        else:
            values = np.asarray(
                shap_values
            )

            if values.ndim == 3:
                values = values[0, :, -1]
            elif values.ndim == 2:
                values = values[0]

        feature_values = np.asarray(
            X.toarray()[0]
            if hasattr(X, "toarray")
            else X[0]
        )

        explanations = []

        for feature, value, shap_value in zip(
            self.feature_names,
            feature_values,
            values,
        ):
            explanations.append(
                {
                    "feature": feature,
                    "value": float(value),
                    "shap_value": float(shap_value),
                    "direction": (
                        "fraud"
                        if shap_value > 0
                        else "genuine"
                    ),
                }
            )

        explanations.sort(
            key=lambda item: abs(
                item["shap_value"]
            ),
            reverse=True,
        )

        return explanations[:top_n]