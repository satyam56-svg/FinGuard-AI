from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.auth.security import hash_password
from backend.app.database.models import User, UserRole


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
) -> User:
    existing_user = db.scalar(
        select(User).where(
            (User.username == username)
            | (User.email == email)
        )
    )

    if existing_user:
        raise ValueError(
            "Username or email is already registered."
        )

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.USER.value,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user