"""
ml_pipeline/preprocessing/preprocessor.py

Preprocessing pipeline for FinGuard AI.

Responsibilities:
- Handle missing numerical values.
- One-hot encode categorical features.
- Learn transformations from training data only.
- Apply the same fitted transformations to validation,
  test, and inference data.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from pathlib import Path
import joblib


class FraudPreprocessor:
    """Prepares engineered PaySim features for ML models."""

    NUMERIC_COLUMNS = (
        "step",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "isFlaggedFraud",
        "origin_balance_error",
        "destination_balance_error",
        "origin_balance_change",
        "destination_balance_change",
    )

    CATEGORICAL_COLUMNS = (
        "type",
    )

    def __init__(self) -> None:

        numeric_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="median"),
                ),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="most_frequent"),
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=True,
                    ),
                ),
            ]
        )

        self._preprocessor = ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    numeric_pipeline,
                    list(self.NUMERIC_COLUMNS),
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    list(self.CATEGORICAL_COLUMNS),
                ),
            ],
            remainder="drop",
        )

        self._is_fitted = False

    def _validate_input(self, X: pd.DataFrame) -> None:

        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame.")

        if X.empty:
            raise ValueError("Input DataFrame cannot be empty.")

        required_columns = (
            list(self.NUMERIC_COLUMNS)
            + list(self.CATEGORICAL_COLUMNS)
        )

        missing_columns = [
            column
            for column in required_columns
            if column not in X.columns
        ]

        if missing_columns:
            raise ValueError(
                "Input DataFrame is missing required columns: "
                f"{missing_columns}"
            )

    def fit(self, X_train: pd.DataFrame) -> "FraudPreprocessor":
        """Learn preprocessing parameters using training data only."""

        self._validate_input(X_train)

        self._preprocessor.fit(X_train)

        self._is_fitted = True

        return self

    def transform(self, X: pd.DataFrame) -> Any:
        """Transform data using the already-fitted preprocessor."""

        if not self._is_fitted:
            raise RuntimeError(
                "FraudPreprocessor has not been fitted. "
                "Call fit() first."
            )

        self._validate_input(X)

        return self._preprocessor.transform(X)

    def fit_transform(
        self,
        X_train: pd.DataFrame,
    ) -> Any:
        """Fit on training data and transform it."""

        self._validate_input(X_train)

        transformed = self._preprocessor.fit_transform(X_train)

        self._is_fitted = True

        return transformed

    def get_feature_names_out(self) -> list[str]:
        """Return names of transformed features."""

        if not self._is_fitted:
            raise RuntimeError(
                "FraudPreprocessor has not been fitted."
            )

        return (
            self._preprocessor
            .get_feature_names_out()
            .tolist()
        )

    def save(self, file_path: str | Path) -> None:
        """Save the fitted preprocessor."""

        if not self._is_fitted:
            raise RuntimeError(
                "Cannot save an unfitted preprocessor."
            )

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self._preprocessor, path)

        print(f"Preprocessor saved to: {path}")


    @classmethod
    def load(cls, file_path: str | Path) -> "FraudPreprocessor":
        """Load a previously fitted preprocessor."""

        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Preprocessor file not found: {path}"
            )

        instance = cls()
        instance._preprocessor = joblib.load(path)
        instance._is_fitted = True

        return instance