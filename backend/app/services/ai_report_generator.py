from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai

from backend.app.schemas import AIReport


load_dotenv()


class AIReportGenerator:
    """Generates controlled AI reports from existing fraud analysis."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not configured."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def generate(
        self,
        prediction_result: dict[str, Any],
    ) -> dict[str, str]:
        """Generate an AI report with a deterministic fallback."""

        if not isinstance(prediction_result, dict):
            raise TypeError(
                "prediction_result must be a dictionary."
            )

        try:
            return self._generate_with_gemini(
                prediction_result
            )

        except Exception:
            # Gemini is an optional explanation layer.
            # Core fraud prediction must remain available
            # when the external AI service is unavailable.
            return self._build_fallback_report(
                prediction_result
            )

    def _generate_with_gemini(
        self,
        prediction_result: dict[str, Any],
    ) -> dict[str, str]:
        """Generate and validate the Gemini report."""

        prompt = self._build_prompt(
            prediction_result
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )

        text = (response.text or "").strip()

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc

        try:
            report = AIReport.model_validate(
                parsed
            )
        except Exception as exc:
            raise RuntimeError(
                "Gemini response did not match the AI report schema."
            ) from exc

        return report.model_dump()

    def _build_fallback_report(
        self,
        prediction_result: dict[str, Any],
    ) -> dict[str, str]:
        """Build a deterministic report without external AI."""

        prediction = prediction_result.get(
            "prediction"
        )

        fraud_probability = float(
            prediction_result.get(
                "fraud_probability",
                0.0,
            )
        )

        risk_score = float(
            prediction_result.get(
                "risk_score",
                0.0,
            )
        )

        risk_level = str(
            prediction_result.get(
                "risk_level",
                "UNKNOWN",
            )
        )

        recommendation = str(
            prediction_result.get(
                "recommendation",
                "UNKNOWN",
            )
        )

        explanation = prediction_result.get(
            "explanation",
            {},
        )

        risk_factors = explanation.get(
            "risk_factors",
            [],
        )

        protective_factors = explanation.get(
            "protective_factors",
            [],
        )

        if prediction == 1:
            assessment = "fraudulent"
        else:
            assessment = "non-fraudulent"

        summary = (
            "The FinGuard AI assessment indicates a "
            f"{risk_level} risk level with a fraud "
            f"probability of {fraud_probability:.6f} "
            f"and a risk score of {risk_score:.2f}. "
            f"The existing prediction is "
            f"{assessment}, with a recommendation to "
            f"{recommendation}."
        )

        risk_reason_parts = []

        if risk_factors:
            risk_reason_parts.append(
                "Risk factors identified by the existing "
                "SHAP analysis: "
                + ", ".join(
                    str(
                        factor.get(
                            "feature",
                            "Unknown feature",
                        )
                    )
                    for factor in risk_factors
                )
                + "."
            )

        if protective_factors:
            risk_reason_parts.append(
                "Protective factors identified by the "
                "existing SHAP analysis: "
                + ", ".join(
                    str(
                        factor.get(
                            "feature",
                            "Unknown feature",
                        )
                    )
                    for factor in protective_factors
                )
                + "."
            )

        if risk_reason_parts:
            risk_reason = " ".join(
                risk_reason_parts
            )
        else:
            risk_reason = (
                "No SHAP risk or protective factors "
                "were available for the explanation."
            )

        return AIReport(
            summary=summary,
            risk_reason=risk_reason,
            recommended_action=recommendation,
        ).model_dump()

    def _build_prompt(
        self,
        prediction_result: dict[str, Any],
    ) -> str:
        """Build a controlled prompt for the AI explanation layer."""

        return f"""
You are the explanation and reporting layer of FinGuard AI.

Your task is ONLY to explain the existing fraud analysis.
You must NOT make a new fraud prediction.
You must NOT change the prediction, fraud probability, risk score,
risk level, or recommendation.

Use ONLY the information explicitly provided below.

Existing FinGuard AI assessment:

Prediction: {prediction_result.get("prediction")}
Fraud probability: {prediction_result.get("fraud_probability")}
Risk score: {prediction_result.get("risk_score")}
Risk level: {prediction_result.get("risk_level")}
Recommendation: {prediction_result.get("recommendation")}

SHAP explanation:
{prediction_result.get("explanation")}

Return ONLY valid JSON with exactly these three string fields:

{{
  "summary": "A concise professional summary of the existing assessment.",
  "risk_reason": "Explain the main risk factors using only the supplied SHAP information.",
  "recommended_action": "State the existing recommendation without changing it."
}}

Strict rules:

1. Do not invent facts.
2. Do not infer account age, user identity, user intent, transaction history,
   location, behavior, or any information not explicitly provided.
3. Do not claim that a feature means something beyond its supplied name,
   value, impact, and direction.
4. Do not create new risk factors.
5. Do not create new protective factors.
6. Do not change the existing recommendation.
7. Do not change the existing risk level.
8. Do not change the existing fraud probability or risk score.
9. Keep the explanation concise and professional.
10. Return JSON only. Do not use Markdown or code fences.
""".strip()