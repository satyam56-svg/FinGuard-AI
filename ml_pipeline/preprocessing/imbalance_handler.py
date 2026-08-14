"""
ml_pipeline/preprocessing/imbalance_handler.py

Handles class imbalance for the FinGuard AI fraud detection pipeline.

Important:
- Only training data should be passed to this module.
- Validation and test data must remain untouched.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.utils.class_weight import compute_class_weight


class ImbalanceHandler:
    """Provides class-weight and resampling utilities."""

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state

    def compute_class_weights(
        self,
        y_train: pd.Series,
    ) -> dict[int, float]:
        """
        Compute balanced class weights from training labels.
        """

        if not isinstance(y_train, pd.Series):
            raise TypeError("y_train must be a pandas Series.")

        if y_train.empty:
            raise ValueError("y_train cannot be empty.")

        classes = np.sort(y_train.unique())

        if len(classes) != 2:
            raise ValueError(
                "ImbalanceHandler currently supports binary classification."
            )

        weights = compute_class_weight(
            class_weight="balanced",
            classes=classes,
            y=y_train,
        )

        return {
            int(label): float(weight)
            for label, weight in zip(classes, weights)
        }

    def get_distribution(
        self,
        y: pd.Series,
    ) -> dict[int, int]:
        """Return class counts without modifying the data."""

        if not isinstance(y, pd.Series):
            raise TypeError("y must be a pandas Series.")

        return {
            int(label): int(count)
            for label, count in y.value_counts().items()
        }