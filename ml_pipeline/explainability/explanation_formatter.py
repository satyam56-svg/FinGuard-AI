"""
ml_pipeline/explainability/explanation_formatter.py

Converts raw SHAP feature contributions into
human-readable fraud explanations.
"""

from __future__ import annotations

from typing import Any


class ExplanationFormatter:
    """Formats SHAP output for application/dashboard consumption."""

    FEATURE_LABELS = {
        "numeric__origin_balance_error": "Origin balance pattern",
        "numeric__destination_balance_error": "Destination balance pattern",
        "numeric__origin_balance_change": "Origin balance change",
        "numeric__destination_balance_change": "Destination balance change",
        "numeric__amount": "Transaction amount",
        "numeric__oldbalanceOrg": "Previous origin balance",
        "numeric__newbalanceOrig": "New origin balance",
        "numeric__oldbalanceDest": "Previous destination balance",
        "numeric__newbalanceDest": "New destination balance",
        "numeric__step": "Transaction time step",
        "numeric__isFlaggedFraud": "Existing fraud flag",
    }

    def format(
        self,
        explanations: list[dict[str, Any]],
        top_n: int = 5,
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Convert SHAP explanations into dashboard-friendly output.
        """

        if not explanations:
            raise ValueError(
                "explanations cannot be empty."
            )

        if top_n <= 0:
            raise ValueError(
                "top_n must be greater than zero."
            )

        risk_factors = []
        protective_factors = []

        for item in explanations:

            shap_value = float(
                item["shap_value"]
            )

            feature = item["feature"]

            # Skip inactive one-hot features.
            if feature.startswith("categorical__"):
                if float(item["value"]) == 0:
                    continue

                feature_name = feature.replace(
                    "categorical__type_",
                    "Transaction type: ",
                )

            else:
                feature_name = self.FEATURE_LABELS.get(
                    feature,
                    feature.replace(
                        "numeric__",
                        "",
                    ),
                )

            formatted = {
                "feature": feature_name,
                "value": item["value"],
                "impact": round(
                    abs(shap_value),
                    6,
                ),
                "direction": (
                    "increases_fraud_risk"
                    if shap_value > 0
                    else "reduces_fraud_risk"
                ),
            }

            if shap_value > 0:
                risk_factors.append(
                    formatted
                )
            elif shap_value < 0:
                protective_factors.append(
                    formatted
                )

        risk_factors.sort(
            key=lambda x: x["impact"],
            reverse=True,
        )

        protective_factors.sort(
            key=lambda x: x["impact"],
            reverse=True,
        )

        return {
            "risk_factors": risk_factors[:top_n],
            "protective_factors": protective_factors[:top_n],
        }