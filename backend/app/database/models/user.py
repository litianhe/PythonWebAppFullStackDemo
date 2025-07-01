import re
from typing import TYPE_CHECKING, List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .comment import Comment


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    comments: List["Comment"] = Relationship(back_populates="user")

    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        if not username:
            raise ValueError("Username cannot be empty")
        if not username.isalnum():
            raise ValueError("Username can only contain letters and numbers")
        if len(username) < 5 or len(username) > 20:
            raise ValueError("Username must be between 5-20 characters")
        return username

    @field_validator("email")
    def validate_email(cls, email: str) -> str:
        if not email:
            raise ValueError("Email cannot be empty")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            raise ValueError("Invalid email format")
        return email


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty")
        if len(password) < 8 or len(password) > 20:
            raise ValueError("Password must be 8-20 characters")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValueError("Password must contain at least one special character")
        return password


class UserResponse(UserBase):
    username: str
    email: str
