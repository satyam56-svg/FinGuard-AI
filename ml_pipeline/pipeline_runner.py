"""
ml_pipeline/pipeline_runner.py

Central orchestrator for the FinGuard AI ML pipeline.

This module coordinates the existing pipeline components.
It does not contain model-specific ML logic.
"""

from __future__ import annotations

from pathlib import Path

import joblib

from ml_pipeline.config.paths import (
    RANDOM_FOREST_MODEL_PATH,
    PREPROCESSOR_PATH,
    MODEL_PATHS,
)

from ml_pipeline.data.data_loader import DataLoader
from ml_pipeline.data.feature_engineering import FeatureEngineer
from ml_pipeline.data.dataset_splitter import DatasetSplitter
from ml_pipeline.preprocessing.preprocessor import FraudPreprocessor


class MLPipelineRunner:
    """Orchestrates the FinGuard AI ML pipeline."""

    def __init__(
        self,
        model_path: str | Path = RANDOM_FOREST_MODEL_PATH,
        preprocessor_path: str | Path = PREPROCESSOR_PATH,
    ) -> None:

        self.model_path = Path(model_path)
        self.preprocessor_path = Path(
            preprocessor_path
        )

        self.data_loader = DataLoader()
        self.feature_engineer = FeatureEngineer()
        self.dataset_splitter = DatasetSplitter()

    def prepare_data(self) -> dict:
        """Load, engineer, split and preprocess dataset."""

        print("\n" + "=" * 70)
        print("FINGUARD AI — PIPELINE DATA PREPARATION")
        print("=" * 70)

        # Load
        print("\n[1/4] Loading dataset...")
        df = self.data_loader.load()

        print(
            f"Dataset shape: {df.shape}"
        )

        # Feature engineering
        print("\n[2/4] Feature engineering...")
        X, y = self.feature_engineer.transform(df)

        print(
            f"Feature shape: {X.shape}"
        )

        # Split
        print("\n[3/4] Splitting dataset...")
        (
            X_train,
            X_val,
            X_test,
            y_train,
            y_val,
            y_test,
        ) = self.dataset_splitter.split(
            X,
            y,
        )

        print(
            f"Train: {X_train.shape}"
        )
        print(
            f"Validation: {X_val.shape}"
        )
        print(
            f"Test: {X_test.shape}"
        )

        # Preprocessing
        print("\n[4/4] Applying preprocessing...")

        preprocessor = FraudPreprocessor()

        X_train_processed = (
            preprocessor.fit_transform(
                X_train
            )
        )

        X_val_processed = (
            preprocessor.transform(
                X_val
            )
        )

        X_test_processed = (
            preprocessor.transform(
                X_test
            )
        )

        print(
            f"Processed features: "
            f"{X_train_processed.shape[1]}"
        )

        return {
            "X_train": X_train_processed,
            "X_val": X_val_processed,
            "X_test": X_test_processed,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test,
            "preprocessor": preprocessor,
        }

    def load_production_model(self):
        """Load the selected production model."""

        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        return joblib.load(
            self.model_path
        )

    def load_production_preprocessor(
        self,
    ) -> FraudPreprocessor:
        """Load the saved production preprocessor."""

        if not self.preprocessor_path.is_file():
            raise FileNotFoundError(
                "Preprocessor not found: "
                f"{self.preprocessor_path}"
            )

        return FraudPreprocessor.load(
            self.preprocessor_path
        )