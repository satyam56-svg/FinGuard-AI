from dataclasses import dataclass


@dataclass(frozen=True)
class MLConfig:
    """Central configuration for the FinGuard AI ML pipeline."""

    # Reproducibility
    random_state: int = 42

    # Target
    target_column: str = "isFraud"

    # Dataset split
    train_size: float = 0.70
    val_size: float = 0.15
    test_size: float = 0.15

    # Models
    model_names: tuple[str, ...] = (
        "logistic_regression",
        "decision_tree",
        "random_forest",
        "xgboost",
        "lightgbm",
    )

    # Evaluation
    primary_metric: str = "f1"
    fraud_threshold: float = 0.60


config = MLConfig()