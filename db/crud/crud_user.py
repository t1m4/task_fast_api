from sqlalchemy.orm import Session

from auth.security import get_password_hash
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


def get_user_is_active(user: User) -> bool:
    return user.is_active

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    print(user.dict())
    db_user = UserDB(**user.dict(), hashed_password=hashed_password)
    print('db', db_user.dict())
    # TODO check that happening with that model. Write tests
    db_user = User(**db_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
