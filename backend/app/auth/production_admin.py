import os

from backend.app.auth.security import hash_password
from backend.app.database.database import SessionLocal
from backend.app.database.models import User, UserRole


def bootstrap_production_admin() -> None:
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not email or not password:
        print(
            "Production admin credentials not configured. "
            "Skipping admin bootstrap."
        )
        return

    db = SessionLocal()

    try:
        existing_admin = (
            db.query(User)
            .filter(User.role == UserRole.ADMIN.value)
            .first()
        )

        if existing_admin:
            print(
                "Production admin already exists. "
                "Skipping admin bootstrap."
            )
            return

        existing_user = (
            db.query(User)
            .filter(
                (User.username == username)
                | (User.email == email)
            )
            .first()
        )

        if existing_user:
            print(
                "Configured admin username/email already belongs "
                "to another user. Skipping admin bootstrap."
            )
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.ADMIN.value,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print(
            f"Production admin created successfully: {username}"
        )

    finally:
        db.close()