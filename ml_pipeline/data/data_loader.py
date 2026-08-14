from pathlib import Path

import pandas as pd

from ml_pipeline.config.paths import PROJECT_ROOT


class DataLoader:
    """Loads the raw PaySim dataset."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self.file_path = (
            Path(file_path)
            if file_path is not None
            else PROJECT_ROOT / "paysim.csv"
        )

    def load(self) -> pd.DataFrame:
        """Load PaySim CSV into a pandas DataFrame."""

        if not self.file_path.is_file():
            raise FileNotFoundError(
                f"Dataset not found: {self.file_path}"
            )

        df = pd.read_csv(self.file_path)

        if df.empty:
            raise ValueError("Dataset is empty.")

        return df