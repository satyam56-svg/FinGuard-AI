"""
ml_pipeline/data/feature_engineering.py

Feature engineering for the PaySim fraud detection dataset.

This module converts raw PaySim transaction data into the
fixed feature contract used by the FinGuard AI ML pipeline.
"""

from __future__ import annotations

import pandas as pd


class FeatureEngineer:
    """
    Creates transaction-level features for fraud detection.

    Raw identifier columns such as nameOrig and nameDest are
    intentionally excluded from the model feature set.
    """

    TARGET_COLUMN = "isFraud"

    REQUIRED_COLUMNS = (
        "step",
        "type",
        "amount",
        "nameOrig",
        "oldbalanceOrg",
        "newbalanceOrig",
        "nameDest",
        "oldbalanceDest",
        "newbalanceDest",
        "isFlaggedFraud",
        "isFraud",
    )

    FEATURE_COLUMNS = (
        "step",
        "type",
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

    def transform(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.Series]:
        """
        Transform raw PaySim data into ML features and target.

        Returns
        -------
        tuple[pd.DataFrame, pd.Series]
            X: engineered features
            y: fraud target
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        if df.empty:
            raise ValueError("Input DataFrame cannot be empty.")

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                "Input dataset is missing required columns: "
                f"{missing_columns}"
            )

        data = df.copy()

        # ---------------------------------------------------------
        # Balance consistency features
        # ---------------------------------------------------------

        data["origin_balance_error"] = (
            data["oldbalanceOrg"]
            - data["amount"]
            - data["newbalanceOrig"]
        )

        data["destination_balance_error"] = (
            data["oldbalanceDest"]
            + data["amount"]
            - data["newbalanceDest"]
        )

        # ---------------------------------------------------------
        # Balance change features
        # ---------------------------------------------------------

        data["origin_balance_change"] = (
            data["oldbalanceOrg"]
            - data["newbalanceOrig"]
        )

        data["destination_balance_change"] = (
            data["newbalanceDest"]
            - data["oldbalanceDest"]
        )

        # ---------------------------------------------------------
        # Separate features and target
        # ---------------------------------------------------------

        X = data[list(self.FEATURE_COLUMNS)].copy()
        y = data[self.TARGET_COLUMN].copy()

        return X, y