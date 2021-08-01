from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from api.dependencies import get_db
from auth.security import create_access_token
from db.crud import crud_user
from db.crud.crud_user import authenticate_user
from schemas import user
from schemas.token import Token
from schemas.user import UserCreate
from task_fast_api.config import settings

router = APIRouter()


@router.get("/", response_model=List[user.UserOut])
def read_users(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=0, le=100),
        # current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve all users.
    - **skip**: Amount of users to skip
    - **limit**: Amount of result
    """
    users = crud_user.get_all_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=user.UserOut)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate,
):
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud_user.create_user(db=db, user=user_in)
    return user


@router.post("/login/token", response_model=Token)
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
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
