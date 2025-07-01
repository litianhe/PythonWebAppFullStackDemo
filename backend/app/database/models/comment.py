from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from .user import UserResponse

if TYPE_CHECKING:
    from .user import User


class CommentBase(SQLModel):
    """Base model containing fields shared across all comment variants"""

    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Comment(CommentBase, table=True):
    """Comment model supporting infinite nesting and eager loading.

    Features:
    - Parent-child relationships for unlimited nesting
    - Eager loading of entire comment tree (selectin)
    - Automatic timestamping
    - Validation for content length
    """

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    parent_id: int = Field(foreign_key="comment.id", default=0)

    # Relationships
    user: "User" = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    children: List["Comment"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={
            "lazy": "selectin",  # Eager loads all nested comments in one query
            "order_by": "Comment.created_at.desc()",  # Newest first
        },
    )
    parent: Optional["Comment"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Comment.id"}
    )

    @field_validator("content")
    def validate_content(cls, content: str) -> str:
        """Validate comment content meets requirements

        Rules:
        - Cannot be empty after stripping whitespace
        - Must be between 3-200 characters (Unicode-aware)
        - Leading/trailing whitespace is automatically stripped
        """
        # Ensure Unicode support by checking character count, not byte length
        content = content.strip()
        if not content:
            raise ValueError("Comment cannot be empty")
        char_count = len(content)
        if char_count < 3 or char_count > 200:
            raise ValueError("Comment must be between 3-200 characters")
        return content


class CommentCreate(CommentBase):
    """Input model for creating new comments via API

    Note: parent_id=0 indicates a root-level comment
    """

    parent_id: int = 0


class CommentResponse(CommentBase):
    """Output model for API responses - includes nested relationships

    Features:
    - Includes user details via UserResponse
    - Recursive children for building comment trees
    - All fields are read-only (output only)
    """

    id: int
    content: str
    created_at: datetime
    user_id: int
    user: UserResponse
    parent_id: int
    children: List["CommentResponse"] = []
