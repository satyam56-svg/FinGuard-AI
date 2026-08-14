"""
ml_pipeline/training/trainer.py

Baseline model training for FinGuard AI.

Models:
- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- LightGBM

Training uses class weights where supported.
Validation and test data are never used during fitting.
"""

from __future__ import annotations

import time
from typing import Any
import joblib
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import xgboost as xgb
import lightgbm as lgb


class ModelTrainer:
    """Trains the registered FinGuard AI baseline models."""

    SUPPORTED_MODELS = (
        "logistic_regression",
        "decision_tree",
        "random_forest",
        "xgboost",
        "lightgbm",
    )

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state

    def _validate_training_data(
        self,
        X_train: Any,
        y_train: pd.Series,
    ) -> None:

        if X_train is None:
            raise ValueError("X_train cannot be None.")

        if getattr(X_train, "shape", (0,))[0] == 0:
            raise ValueError("X_train cannot be empty.")

        if not isinstance(y_train, pd.Series):
            raise TypeError("y_train must be a pandas Series.")

        if y_train.empty:
            raise ValueError("y_train cannot be empty.")

        if X_train.shape[0] != len(y_train):
            raise ValueError(
                "X_train and y_train must contain the same number "
                "of samples."
            )

        if y_train.nunique() != 2:
            raise ValueError(
                "FinGuard AI currently supports binary classification."
            )

    def _build_model(
        self,
        model_name: str,
        class_weights: dict[int, float],
    ) -> Any:

        if model_name == "logistic_regression":
            return LogisticRegression(
                max_iter=1000,
                random_state=self.random_state,
                class_weight=class_weights,
                solver="liblinear",
            )

        if model_name == "decision_tree":
            return DecisionTreeClassifier(
                max_depth=10,
                random_state=self.random_state,
                class_weight=class_weights,
            )

        if model_name == "random_forest":
            return RandomForestClassifier(
                n_estimators=150,
                max_depth=12,
                random_state=self.random_state,
                class_weight=class_weights,
                n_jobs=-1,
            )

        if model_name == "xgboost":
            return xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                eval_metric="logloss",
                n_jobs=-1,
                scale_pos_weight=(
                    class_weights[1] / class_weights[0]
                ),
            )

        if model_name == "lightgbm":
            return lgb.LGBMClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                n_jobs=-1,
                verbose=-1,
                scale_pos_weight=(
                    class_weights[1] / class_weights[0]
                ),
            )

        raise ValueError(
            f"Unsupported model '{model_name}'. "
            f"Supported models: {self.SUPPORTED_MODELS}"
        )

    def train(
        self,
        model_name: str,
        X_train: Any,
        y_train: pd.Series,
        class_weights: dict[int, float],
    ) -> tuple[Any, float]:

        self._validate_training_data(
            X_train,
            y_train,
        )

        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model '{model_name}'."
            )

        if not class_weights:
            raise ValueError(
                "class_weights cannot be empty."
            )

        model = self._build_model(
            model_name,
            class_weights,
        )

        print(
            f"\nTraining {model_name}..."
        )

        start_time = time.perf_counter()

        model.fit(
            X_train,
            y_train,
        )

        training_time = (
            time.perf_counter() - start_time
        )

        print(
            f"Completed {model_name} "
            f"in {training_time:.2f} seconds."
        )

        return model, training_time

    def save_model(
        self,
        model: Any,
        file_path: str | Path,
    ) -> None:
        """Save a trained model to disk."""

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(model, path)

        print(f"Model saved to: {path}")