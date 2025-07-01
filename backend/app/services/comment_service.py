"""Service layer for comment operations - handles business logic for comments"""
from typing import List

from sqlmodel import Session

from app.database.models.comment import Comment, CommentCreate


def create_comment(db: Session, comment_create: CommentCreate, user_id: int) -> Comment:
    """Create a new comment in the database

    Args:
        db: Database session
        comment_create: Comment data from API request
        user_id: ID of the user creating the comment

    Returns:
        The created Comment object with database-generated fields
    """
    db_comment = Comment(
        content=comment_create.content,
        user_id=user_id,
        parent_id=comment_create.parent_id if comment_create.parent_id else 0,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_tree(db: Session) -> List[Comment]:
    """Build and return a hierarchical tree structure of all comments

    Algorithm:
    1. Fetch all comments from DB (newest first)
    2. Create a lookup dictionary by comment ID
    3. Identify root comments (no parent)
    4. Attach child comments to their parents recursively

    Args:
        db: Database session

    Returns:
        List of root comments, each with their children attached
    """
    # Get all comments with pre-loaded children (sorted by created_at.desc via model definition)
    comments = db.query(Comment).order_by(Comment.created_at.desc()).all()
    
    # Dictionary for O(1) comment lookups
    comment_dict = {comment.id: comment for comment in comments}
    root_comments = []
    
    # Build tree structure
    for comment in comments:
        # Root comment
        if comment.parent_id == 0:
            root_comments.append(comment)
        else:
            parent = comment_dict.get(comment.parent_id)
            if parent and hasattr(parent, 'children'):
                # Prevent duplicates
                if comment not in parent.children:
                    parent.children.append(comment)
    
    return root_comments


def get_comment(db: Session, comment_id: int) -> Comment:
    """Get a single comment by ID

    Args:
        db: Database session
        comment_id: ID of comment to retrieve

    Returns:
        The Comment object or None if not found
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()
