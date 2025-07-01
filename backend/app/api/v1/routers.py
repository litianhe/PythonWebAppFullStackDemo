"""API router configuration - defines all API endpoints and their security requirements"""
from fastapi import APIRouter, Depends

from app.api.v1.endpoints import auth, comment, user
from app.core.security import get_current_user

# Main router instance that will be included in the FastAPI app
api_router = APIRouter()

# Public routes - accessible without authentication
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected routes - require valid authentication
# Note: Comment routes are currently public (auth dependency commented out)
# Uncomment to require authentication for comment endpoints
api_router.include_router(
    comment.router,
    prefix="/comments",
    tags=["comments"],
    # dependencies=[Depends(get_current_user)]
)
# User routes always require authentication
api_router.include_router(
    user.router, prefix="/user", tags=["user"], dependencies=[Depends(get_current_user)]
)
