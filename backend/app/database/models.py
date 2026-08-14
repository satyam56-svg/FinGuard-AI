from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class UserRole(str, Enum):
    USER = "USER"
    ANALYST = "ANALYST"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default=UserRole.USER.value,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

class PredictionAudit(Base):
    __tablename__ = "prediction_audits"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    prediction: Mapped[int] = mapped_column(
        nullable=False,
    )

    fraud_probability: Mapped[float] = mapped_column(
        nullable=False,
    )

    risk_score: Mapped[float] = mapped_column(
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    recommendation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )