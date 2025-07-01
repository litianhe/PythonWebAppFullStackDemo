from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import get_password_hash
from app.database.models.user import User, UserCreate


def create_user(db: Session, user_create: UserCreate):
    # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter(
            (User.username == user_create.username) | (User.email == user_create.email)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    # Hash password
    hashed_password = get_password_hash(user_create.password)

    # Create user
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
