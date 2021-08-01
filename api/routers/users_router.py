from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from db.crud import crud_user
from schemas import user
from schemas.user import UserCreate

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
