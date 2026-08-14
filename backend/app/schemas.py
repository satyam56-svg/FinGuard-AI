from enum import Enum

from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"
    DEBIT = "DEBIT"
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"


class TransactionRequest(BaseModel):
    step: int
    type: TransactionType

    amount: float = Field(ge=0)

    oldbalanceOrg: float = Field(ge=0)
    newbalanceOrig: float = Field(ge=0)

    oldbalanceDest: float = Field(ge=0)
    newbalanceDest: float = Field(ge=0)

    isFlaggedFraud: int = Field(
        ge=0,
        le=1,
    )

    origin_balance_error: float
    destination_balance_error: float

    origin_balance_change: float
    destination_balance_change: float

class ExplanationFactor(BaseModel):
    feature: str
    value: float
    impact: float
    direction: str


class Explanation(BaseModel):
    risk_factors: list[ExplanationFactor]
    protective_factors: list[ExplanationFactor]

class AIReport(BaseModel):
    summary: str
    risk_reason: str
    recommended_action: str

class PredictionResponse(BaseModel):
    prediction: int
    fraud_probability: float
    risk_score: float
    risk_level: str
    recommendation: str
    explanation: Explanation
    ai_report: AIReport

class UserRegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )

    email: str = Field(
        min_length=5,
        max_length=255,
    )

    password: str = Field(
        min_length=8,
        max_length=72,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool

class RoleUpdateRequest(BaseModel):
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserStatusUpdateRequest(BaseModel):
    is_active: bool

class PredictionHistoryResponse(BaseModel):
    id: int
    prediction: int
    fraud_probability: float
    risk_score: float
    risk_level: str
    recommendation: str

class DashboardStatsResponse(BaseModel):
    total_predictions: int
    fraud_predictions: int
    non_fraud_predictions: int
    fraud_rate: float
    average_risk_score: float

class RiskDistributionResponse(BaseModel):
    low: int
    medium: int
    high: int
    critical: int

class RecentPredictionResponse(BaseModel):
    id: int
    prediction: int
    fraud_probability: float
    risk_score: float
    risk_level: str
    recommendation: str