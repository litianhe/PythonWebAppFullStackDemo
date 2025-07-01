from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.security import get_current_user
from app.database.models.user import User

router = APIRouter()


@router.get("/me")
async def read_current_user(
    request: Request, current_user: Annotated[User, Depends(get_current_user)]
):
    return {"username": current_user.username, "email": current_user.email}
