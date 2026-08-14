"""
ml_pipeline/evaluation/threshold_analyzer.py

Analyzes classification thresholds for fraud detection.

Threshold selection is performed ONLY on validation data.
The test set must never be used for threshold selection.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)


class ThresholdAnalyzer:
    """Analyze precision-recall trade-offs across thresholds."""

    def analyze(
        self,
        y_true: Any,
        y_prob: Any,
        thresholds: list[float] | None = None,
    ) -> pd.DataFrame:

        y_true = np.asarray(y_true)
        y_prob = np.asarray(y_prob)

        if len(y_true) != len(y_prob):
            raise ValueError(
                "y_true and y_prob must have the same length."
            )

        if thresholds is None:
            thresholds = [
                0.10,
                0.20,
                0.30,
                0.40,
                0.50,
                0.60,
                0.70,
                0.80,
                0.90,
                0.95,
                0.99,
            ]

        results = []

        for threshold in thresholds:

            y_pred = (
                y_prob >= threshold
            ).astype(int)

            precision = precision_score(
                y_true,
                y_pred,
                zero_division=0,
            )

            recall = recall_score(
                y_true,
                y_pred,
                zero_division=0,
            )

            f1 = f1_score(
                y_true,
                y_pred,
                zero_division=0,
            )

            false_positives = int(
                ((y_true == 0) & (y_pred == 1)).sum()
            )

            false_negatives = int(
                ((y_true == 1) & (y_pred == 0)).sum()
            )

            results.append(
                {
                    "threshold": threshold,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "false_positives": false_positives,
                    "false_negatives": false_negatives,
                }
            )

        return pd.DataFrame(results)

    def find_best_f1(
        self,
        results: pd.DataFrame,
    ) -> dict[str, float]:

        if results.empty:
            raise ValueError(
                "Threshold results cannot be empty."
            )

        best = results.loc[
            results["f1"].idxmax()
        ]

        return {
            "threshold": float(best["threshold"]),
            "precision": float(best["precision"]),
            "recall": float(best["recall"]),
            "f1": float(best["f1"]),
            "false_positives": int(
                best["false_positives"]
            ),
            "false_negatives": int(
                best["false_negatives"]
            ),
        }