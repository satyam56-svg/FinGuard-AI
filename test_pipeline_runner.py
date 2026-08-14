from ml_pipeline.pipeline_runner import MLPipelineRunner


runner = MLPipelineRunner()

data = runner.prepare_data()

print("\n" + "=" * 70)
print("PIPELINE RUNNER TEST")
print("=" * 70)

print(
    "Train:",
    data["X_train"].shape,
    data["y_train"].shape,
)

print(
    "Validation:",
    data["X_val"].shape,
    data["y_val"].shape,
)

print(
    "Test:",
    data["X_test"].shape,
    data["y_test"].shape,
)

print(
    "Preprocessor:",
    type(data["preprocessor"]).__name__,
)

print("\nPipeline runner working successfully.")