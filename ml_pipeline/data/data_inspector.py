import pandas as pd


class DatasetInspector:
    """Inspects the structure and quality of the PaySim dataset."""

    def inspect(self, df: pd.DataFrame) -> dict:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        if df.empty:
            raise ValueError("Cannot inspect an empty dataset.")

        report = {
            "shape": {
                "rows": int(df.shape[0]),
                "columns": int(df.shape[1]),
            },
            "columns": df.columns.tolist(),
            "dtypes": {
                column: str(dtype)
                for column, dtype in df.dtypes.items()
            },
            "missing_values": {
                column: int(count)
                for column, count in df.isnull().sum().items()
                if count > 0
            },
            "duplicate_rows": int(df.duplicated().sum()),
        }

        if "isFraud" in df.columns:
            counts = df["isFraud"].value_counts()

            report["class_distribution"] = {
                str(label): {
                    "count": int(count),
                    "percentage": float(
                        count / len(df) * 100
                    ),
                }
                for label, count in counts.items()
            }

        return report