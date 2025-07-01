from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session

from app.core.security import get_current_user
from app.database.models.comment import Comment, CommentCreate, CommentResponse
from app.database.models.user import User
from app.database.session import get_dbsession
from app.services.comment_service import (create_comment, get_comment,
                                          get_comments_tree)

router = APIRouter()


@router.post("/", response_model=Comment)
async def create_new_comment(
    request: Request,
    comment_create: CommentCreate,
    db: Session = Depends(get_dbsession),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_comment(db, comment_create, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[CommentResponse])
async def get_all_comments(
    request: Request,
    db: Session = Depends(get_dbsession),
):
    return get_comments_tree(db)


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_single_comment(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_dbsession),
    # current_user: User = Depends(get_current_user),
):
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comment
