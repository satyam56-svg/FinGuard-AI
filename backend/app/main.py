from fastapi import FastAPI, HTTPException
from typing import Any
from ml_pipeline.inference.predictor import FraudPredictor
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import (
    TransactionRequest,
    PredictionResponse,
)
from fastapi import Request
from fastapi.responses import JSONResponse




app = FastAPI(
    title="FinGuard AI API",
    description="Fraud Detection and Risk Assessment API",
    version="1.0.0",
)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error."
        },
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://finguard-ai-4ico.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load production ML pipeline
predictor = FraudPredictor()
from backend.app.services.ai_report_generator import (
    AIReportGenerator,
)
ai_report_generator = AIReportGenerator()

@app.get("/")
def root():
    return {
        "message": "FinGuard AI API is running",
        "status": "healthy",
    }


@app.api_route(
    "/health",
    methods=["GET", "HEAD"],
    summary="Check API health",
)
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Analyze a transaction for fraud",
    description=(
        "Runs the FinGuard AI fraud detection pipeline "
        "and returns fraud probability, risk assessment, "
        "and explainability factors."
    ),
    response_description="Fraud detection and risk assessment result",
)
def predict(
    transaction: TransactionRequest,
) -> dict[str, Any]:
    try:
        result = predictor.predict(
            transaction.model_dump()
        )

        result["ai_report"] = ai_report_generator.generate(
            result
        )

        return result

    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc





