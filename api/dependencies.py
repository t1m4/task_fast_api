from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from auth import security
from db import models
from db.crud import crud_user
from db.database import SessionLocal
from schemas.token import TokenPayload
from task_fast_api.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"users/login/token"
)


def get_db() -> Generator:
    """
    Create and close DB Session for each request
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Check user's jwt token
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud_user.get_user(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
