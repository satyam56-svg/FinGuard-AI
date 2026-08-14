from getpass import getpass

from backend.app.auth.security import hash_password
from backend.app.database.database import SessionLocal
from backend.app.database.models import User, UserRole


def bootstrap_analyst() -> None:
    db = SessionLocal()

    try:
        username = input("Analyst username: ").strip()
        email = input("Analyst email: ").strip()
        password = getpass("Analyst password: ")

        if not username or not email or not password:
            raise ValueError(
                "Username, email, and password are required."
            )

        existing_user = (
            db.query(User)
            .filter(
                (User.username == username)
                | (User.email == email)
            )
            .first()
        )

        if existing_user:
            raise ValueError(
                "Username or email is already registered."
            )

        analyst = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.ANALYST.value,
            is_active=True,
        )

        db.add(analyst)
        db.commit()
        db.refresh(analyst)

        print("Analyst created successfully.")
        print(f"Username: {analyst.username}")
        print(f"Role: {analyst.role}")

    finally:
        db.close()


if __name__ == "__main__":
    bootstrap_analyst()