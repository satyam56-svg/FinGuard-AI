"""
ml_pipeline/data/dataset_splitter.py

Creates stratified train, validation, and test splits
for the FinGuard AI fraud detection pipeline.
"""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetSplitter:
    """Creates reproducible stratified dataset splits."""

    def __init__(
        self,
        train_size: float = 0.70,
        validation_size: float = 0.15,
        test_size: float = 0.15,
        random_state: int = 42,
    ) -> None:

        total = train_size + validation_size + test_size

        if abs(total - 1.0) > 1e-9:
            raise ValueError(
                "train_size + validation_size + test_size must equal 1.0."
            )

        if min(train_size, validation_size, test_size) <= 0:
            raise ValueError(
                "All split sizes must be greater than 0."
            )

        self.train_size = train_size
        self.validation_size = validation_size
        self.test_size = test_size
        self.random_state = random_state

    def split(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.Series,
        pd.Series,
        pd.Series,
    ]:
        """
        Create stratified train, validation, and test datasets.
        """

        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame.")

        if not isinstance(y, pd.Series):
            raise TypeError("y must be a pandas Series.")

        if X.empty:
            raise ValueError("X cannot be empty.")

        if y.empty:
            raise ValueError("y cannot be empty.")

        if len(X) != len(y):
            raise ValueError(
                "X and y must contain the same number of rows."
            )

        # ---------------------------------------------------------
        # First split: Train vs temporary set
        # ---------------------------------------------------------

        temp_size = self.validation_size + self.test_size

        X_train, X_temp, y_train, y_temp = train_test_split(
            X,
            y,
            test_size=temp_size,
            random_state=self.random_state,
            stratify=y,
        )

        # ---------------------------------------------------------
        # Second split: Validation vs Test
        # ---------------------------------------------------------

        test_ratio_inside_temp = (
            self.test_size / temp_size
        )

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp,
            y_temp,
            test_size=test_ratio_inside_temp,
            random_state=self.random_state,
            stratify=y_temp,
        )

        return (
            X_train,
            X_val,
            X_test,
            y_train,
            y_val,
            y_test,
        )