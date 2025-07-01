from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.security import authenticate_user, create_access_token
from app.database.models.user import UserCreate
from app.database.session import get_dbsession
from app.services.user_service import create_user

router = APIRouter()


@router.post("/register")
async def register(user_create: UserCreate, db: Session = Depends(get_dbsession)):
    try:
        _ = create_user(db, user_create)
        return {"message": "User created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_dbsession),
):
    # Try username first, then email
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        user = authenticate_user(
            db, form_data.username, form_data.password
        )  # Try as email

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Set token expiration based on "remember me"
    remember_me = form_data.scopes and "remember_me" in form_data.scopes
    access_token_expires = timedelta(days=30) if remember_me else timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email,
    }


@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
