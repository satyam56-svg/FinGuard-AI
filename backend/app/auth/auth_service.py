from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.auth.security import (
    create_access_token,
    verify_password,
)
from backend.app.database.models import User


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    user = db.scalar(
        select(User).where(
            User.username == username
        )
    )

    if user is None:
        raise ValueError(
            "Invalid username or password."
        )

    if not user.is_active:
        raise ValueError(
            "User account is inactive."
        )

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise ValueError(
            "Invalid username or password."
        )

    return user


def login_user(
    db: Session,
    username: str,
    password: str,
) -> str:
    user = authenticate_user(
        db=db,
        username=username,
        password=password,
    )

    return create_access_token(
        {
            "sub": user.username,
            "role": user.role,
        }
    )