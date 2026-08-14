"""
ml_pipeline/evaluation/evaluator.py

Evaluates binary fraud classification models on validation/test data.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)


class ModelEvaluator:
    """Evaluates FinGuard AI classification models."""

    def evaluate(
        self,
        model: Any,
        X,
        y_true,
    ) -> dict[str, Any]:

        if X is None or X.shape[0] == 0:
            raise ValueError("X cannot be empty.")

        if y_true is None or len(y_true) == 0:
            raise ValueError("y_true cannot be empty.")

        if X.shape[0] != len(y_true):
            raise ValueError(
                "X and y_true must contain the same number of samples."
            )

        y_true = np.asarray(y_true)

        # Class prediction
        y_pred = model.predict(X)

        # Fraud probability
        if not hasattr(model, "predict_proba"):
            raise ValueError(
                "Model must provide predict_proba() for fraud evaluation."
            )

        y_prob = model.predict_proba(X)[:, 1]

        # Classification metrics
        accuracy = accuracy_score(y_true, y_pred)
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

        roc_auc = roc_auc_score(
            y_true,
            y_prob,
        )

        pr_auc = average_precision_score(
            y_true,
            y_prob,
        )

        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(
            y_true,
            y_pred,
            labels=[0, 1],
        ).ravel()

        return {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "roc_auc": float(roc_auc),
            "pr_auc": float(pr_auc),
            "confusion_matrix": {
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp),
            },
        }