from getpass import getpass

from backend.app.auth.security import hash_password
from backend.app.database.database import SessionLocal
from backend.app.database.models import User, UserRole


def bootstrap_admin() -> None:
    db = SessionLocal()

    try:
        username = input("Admin username: ").strip()
        email = input("Admin email: ").strip()
        password = getpass("Admin password: ")

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

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.ADMIN.value,
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin created successfully.")
        print(f"Username: {admin.username}")
        print(f"Role: {admin.role}")

    finally:
        db.close()


if __name__ == "__main__":
    bootstrap_admin()