from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.database.models import User, UserRole

def get_all_users(db: Session) -> list[User]:
    return list(
        db.scalars(
            select(User).order_by(User.id)
        ).all()
    )

def update_user_role(
    db: Session,
    user_id: int,
    new_role: str,
    current_admin_id: int,
) -> User:

    user = db.get(User, user_id)

    if user is None:
        raise ValueError("User not found.")

    allowed_roles = {
        UserRole.USER.value,
        UserRole.ANALYST.value,
        UserRole.ADMIN.value,
    }

    if new_role not in allowed_roles:
        raise ValueError(
            "Invalid role. Allowed roles: USER, ANALYST, ADMIN."
        )

    if user.id == current_admin_id:
        raise ValueError(
            "Admin cannot change their own role."
        )

    user.role = new_role

    db.commit()
    db.refresh(user)

    return user

def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool,
    current_admin_id: int,
) -> User:

    user = db.get(User, user_id)

    if user is None:
        raise ValueError("User not found.")

    if user.id == current_admin_id and not is_active:
        raise ValueError(
            "Admin cannot deactivate their own account."
        )

    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return user