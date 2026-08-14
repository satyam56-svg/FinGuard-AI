from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_PIPELINE_DIR = PROJECT_ROOT / "ml_pipeline"

DATA_DIR = ML_PIPELINE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = ML_PIPELINE_DIR / "models"
REPORTS_DIR = ML_PIPELINE_DIR / "reports"
FIGURES_DIR = ML_PIPELINE_DIR / "figures"
LOGS_DIR = ML_PIPELINE_DIR / "logs"


# Model artifacts
RANDOM_FOREST_MODEL_PATH = MODELS_DIR / "random_forest.pkl"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"

MODEL_PATHS = {
    "logistic_regression": MODELS_DIR / "logistic_regression.pkl",
    "decision_tree": MODELS_DIR / "decision_tree.pkl",
    "random_forest": MODELS_DIR / "random_forest.pkl",
    "xgboost": MODELS_DIR / "xgboost.pkl",
    "lightgbm": MODELS_DIR / "lightgbm.pkl",
}


# Create required directories
for directory in (
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    LOGS_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
