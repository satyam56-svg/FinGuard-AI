from fastapi import FastAPI, HTTPException
from typing import Any
from ml_pipeline.inference.predictor import FraudPredictor
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import (
    TransactionRequest,
    PredictionResponse,
    UserRegisterRequest,
    UserResponse,
    LoginRequest,
    TokenResponse,
    AdminUserResponse,
    RoleUpdateRequest,
    UserStatusUpdateRequest,
    PredictionHistoryResponse,
    DashboardStatsResponse,
    RiskDistributionResponse,
    RecentPredictionResponse,
)
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import JSONResponse

from backend.app.auth.user_service import create_user
from backend.app.database.database import (
    get_db,
    init_db,
)
from backend.app.auth.auth_service import login_user
from backend.app.auth.security import get_current_user
from backend.app.auth.authorization import require_roles
from backend.app.database.models import User
from backend.app.auth.admin_service import (
    get_all_users,
    update_user_role,
    update_user_status,
)
from backend.app.services.prediction_audit_service import (
    create_prediction_audit,
    get_user_prediction_history,
)

from backend.app.services.dashboard_service import (
    get_dashboard_stats,
    get_risk_distribution,
    get_recent_predictions,
)

app = FastAPI(
    title="FinGuard AI API",
    description="Fraud Detection and Risk Assessment API",
    version="1.0.0",
)

@app.on_event("startup")
def startup():
    init_db()

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


@app.get(
    "/health",
    summary="Check API health",
)
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
    }


@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
)
def register(
    user: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    try:
        created_user = create_user(
            db=db,
            username=user.username,
            email=user.email,
            password=user.password,
        )

        return UserResponse(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            role=created_user.role,
            is_active=created_user.is_active,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

@app.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Login and obtain an access token",
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        token = login_user(
            db=db,
            username=credentials.username,
            password=credentials.password,
        )

        return TokenResponse(
            access_token=token,
            token_type="bearer",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc

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
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    try:
        result = predictor.predict(
            transaction.model_dump()
        )

        result["ai_report"] = ai_report_generator.generate(
            result
        )

        user = db.query(User).filter(
            User.username == current_user["sub"]
        ).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Authenticated user not found.",
            )

        create_prediction_audit(
            db=db,
            user_id=user.id,
            prediction_result=result,
        )

        return result

    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.get(
    "/predictions/history",
    response_model=list[PredictionHistoryResponse],
    summary="Get current user's prediction history",
)
def prediction_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[PredictionHistoryResponse]:

    user = db.query(User).filter(
        User.username == current_user["sub"]
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user not found.",
        )

    history = get_user_prediction_history(
        db=db,
        user_id=user.id,
    )

    return [
        PredictionHistoryResponse(
            id=audit.id,
            prediction=audit.prediction,
            fraud_probability=audit.fraud_probability,
            risk_score=audit.risk_score,
            risk_level=audit.risk_level,
            recommendation=audit.recommendation,
        )
        for audit in history
    ]


@app.get(
    "/analyst/dashboard",
    summary="Analyst-only access",
)
def analyst_dashboard(
    current_user: dict = Depends(
        require_roles("ANALYST", "ADMIN")
    ),
) -> dict[str, Any]:
    return {
        "message": "Analyst dashboard access granted.",
        "username": current_user["sub"],
        "role": current_user["role"],
    }

@app.get(
    "/analyst/dashboard/stats",
    response_model=DashboardStatsResponse,
    summary="Get dashboard statistics",
)
def analyst_dashboard_stats(
    current_user: dict = Depends(
        require_roles("ANALYST", "ADMIN")
    ),
    db: Session = Depends(get_db),
) -> DashboardStatsResponse:

    stats = get_dashboard_stats(db)

    return DashboardStatsResponse(**stats)


@app.get(
    "/analyst/dashboard/risk-distribution",
    response_model=RiskDistributionResponse,
    summary="Get risk distribution",
)
def analyst_risk_distribution(
    current_user: dict = Depends(
        require_roles("ANALYST", "ADMIN")
    ),
    db: Session = Depends(get_db),
) -> RiskDistributionResponse:

    distribution = get_risk_distribution(db)

    return RiskDistributionResponse(**distribution)

@app.get(
    "/analyst/dashboard/recent-predictions",
    response_model=list[RecentPredictionResponse],
    summary="Get recent predictions",
)
def analyst_recent_predictions(
    current_user: dict = Depends(
        require_roles("ANALYST", "ADMIN")
    ),
    db: Session = Depends(get_db),
) -> list[RecentPredictionResponse]:

    predictions = get_recent_predictions(db)

    return [
        RecentPredictionResponse(
            id=prediction.id,
            prediction=prediction.prediction,
            fraud_probability=prediction.fraud_probability,
            risk_score=prediction.risk_score,
            risk_level=prediction.risk_level,
            recommendation=prediction.recommendation,
        )
        for prediction in predictions
    ]


@app.get(
    "/admin/dashboard",
    summary="Admin-only access",
)
def admin_dashboard(
    current_user: dict = Depends(
        require_roles("ADMIN")
    ),
) -> dict[str, Any]:
    return {
        "message": "Admin dashboard access granted.",
        "username": current_user["sub"],
        "role": current_user["role"],
    }

@app.get(
    "/admin/users",
    response_model=list[AdminUserResponse],
    summary="List all users",
)
def list_users(
    current_user: dict = Depends(
        require_roles("ADMIN")
    ),
    db: Session = Depends(get_db),
) -> list[AdminUserResponse]:

    users = get_all_users(db)

    return [
        AdminUserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )
        for user in users
    ]

@app.patch(
    "/admin/users/{user_id}/role",
    response_model=AdminUserResponse,
    summary="Update a user's role",
)
def update_role(
    user_id: int,
    role_request: RoleUpdateRequest,
    current_user: dict = Depends(
        require_roles("ADMIN")
    ),
    db: Session = Depends(get_db),
) -> AdminUserResponse:

    try:
        admin_user = db.query(User).filter(
            User.username == current_user["sub"]
        ).first()

        if admin_user is None:
            raise HTTPException(
                status_code=401,
                detail="Authenticated admin user not found.",
            )

        updated_user = update_user_role(
            db=db,
            user_id=user_id,
            new_role=role_request.role,
            current_admin_id=admin_user.id,
        )

        return AdminUserResponse(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            role=updated_user.role,
            is_active=updated_user.is_active,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

@app.patch(
    "/admin/users/{user_id}/status",
    response_model=AdminUserResponse,
    summary="Activate or deactivate a user",
)
def update_status(
    user_id: int,
    status_request: UserStatusUpdateRequest,
    current_user: dict = Depends(
        require_roles("ADMIN")
    ),
    db: Session = Depends(get_db),
) -> AdminUserResponse:

    try:
        admin_user = db.query(User).filter(
            User.username == current_user["sub"]
        ).first()

        if admin_user is None:
            raise HTTPException(
                status_code=401,
                detail="Authenticated admin user not found.",
            )

        updated_user = update_user_status(
            db=db,
            user_id=user_id,
            is_active=status_request.is_active,
            current_admin_id=admin_user.id,
        )

        return AdminUserResponse(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            role=updated_user.role,
            is_active=updated_user.is_active,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc