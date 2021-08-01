from sqlalchemy.orm import Session

from auth.security import get_password_hash, verify_password
from db.models.user import User
from schemas.user import UserCreate, UserDB


def get_user(db: Session, user_id: int):
    """
    Get user using user_id
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Get user by email
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Get user by email
    """
    return db.query(User).filter(User.username == username).first()


def get_user_is_active(user: User) -> bool:
    return user.is_active


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(**user.dict(), hashed_password=hashed_password)
    db_user = User(**db_user.dict())
    db.add(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
