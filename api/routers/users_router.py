from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from api.dependencies import get_db, get_current_user, get_current_user_is_superuser
from auth.security import create_access_token
from db.crud import crud_user
from db.crud.crud_user import authenticate_user
from db.models import User
from schemas import user
from schemas.token import Token
from schemas.user import UserCreate
from task_fast_api.config import settings

router = APIRouter()


@router.get("/", response_model=List[user.UserOut])
def get_users(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=0, le=100),
        current_user: User = Depends(get_current_user_is_superuser)
):
    """
    Retrieve all users.
    - **skip**: Amount of users to skip
    - **limit**: Amount of result
    """
    return crud_user.get_all_users(db, skip=skip, limit=limit)


@router.post("/", response_model=user.UserOut)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate,
):
    """
    Create new user
    """
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user_in)


@router.post("/login/token", response_model=Token)
def get_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Get access token for login
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me', response_model=user.UserOut)
def check_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current user
    """
    return current_user
