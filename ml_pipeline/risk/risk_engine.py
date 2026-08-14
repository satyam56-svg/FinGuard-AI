"""
ml_pipeline/risk/risk_engine.py

Converts ML fraud probability into an application-level
risk score, risk level, and recommendation.

The Risk Engine does NOT retrain or modify the ML model.
"""

from __future__ import annotations

from dataclasses import dataclass
from ml_pipeline.config.config import config


@dataclass(frozen=True)
class RiskResult:
    """Final application-level risk decision."""

    fraud_probability: float
    risk_score: float
    risk_level: str
    recommendation: str


class RiskEngine:
    """
    Converts fraud probability into a normalized risk score.

    Risk score:
        0   -> lowest risk
        100 -> highest risk
    """

    def __init__(
        self,
        fraud_threshold: float = config.fraud_threshold,
    ) -> None:

        if not 0.0 <= fraud_threshold <= 1.0:
            raise ValueError(
                "fraud_threshold must be between 0 and 1."
            )

        self.fraud_threshold = fraud_threshold

    def calculate_risk_score(
        self,
        fraud_probability: float,
    ) -> float:
        """Convert probability into a 0-100 risk score."""

        if not 0.0 <= fraud_probability <= 1.0:
            raise ValueError(
                "fraud_probability must be between 0 and 1."
            )

        return round(
            fraud_probability * 100.0,
            2,
        )

    def get_risk_level(
        self,
        fraud_probability: float,
    ) -> str:
        """
        Convert fraud probability into risk level.

        LOW      < 0.20
        MEDIUM   < 0.40
        HIGH     < 0.60
        CRITICAL >= 0.60
        """

        if fraud_probability < 0.20:
            return "LOW"

        if fraud_probability < 0.40:
            return "MEDIUM"

        if fraud_probability < self.fraud_threshold:
            return "HIGH"

        return "CRITICAL"

    def get_recommendation(
        self,
        fraud_probability: float,
    ) -> str:
        """Generate an application-level recommendation."""

        if fraud_probability < 0.20:
            return "ALLOW"

        if fraud_probability < 0.40:
            return "ALLOW_WITH_MONITORING"

        if fraud_probability < self.fraud_threshold:
            return "REVIEW"

        return "BLOCK_OR_REVIEW"

    def evaluate(
        self,
        fraud_probability: float,
    ) -> RiskResult:
        """Generate the complete risk decision."""

        risk_score = self.calculate_risk_score(
            fraud_probability
        )

        risk_level = self.get_risk_level(
            fraud_probability
        )

        recommendation = self.get_recommendation(
            fraud_probability
        )

        return RiskResult(
            fraud_probability=fraud_probability,
            risk_score=risk_score,
            risk_level=risk_level,
            recommendation=recommendation,
        )