from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.base_classes import Base
from db.crud.crud_user import create_user
from db.models import User
from schemas.user import UserCreate
from task_fast_api.config import settings

# create test db
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_TEST_URI)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(autouse=True)
def check(db: Session):
    yield
    users = db.query(User).all()
    for i in users:
        db.delete(i)
    db.commit()


test_user_data = {
    'username': 'test',
    'password': 'test',
    'email': 'test@mail.ru',
}


def test_create_user(db: Session):
    user_in = UserCreate(**test_user_data)
    user = create_user(db, user_in)
    assert user.email == test_user_data['email']
    assert hasattr(user, "hashed_password")
    assert user.is_active == True
    assert user.is_superuser == False


def test_create_user_active(db: Session):
    user_in = UserCreate(**test_user_data, is_active=True)
    user = create_user(db, user_in)
    assert user.is_active == True


def test_create_user_is_superuser(db: Session):
    user_in = UserCreate(**test_user_data, is_superuser=True)
    user = create_user(db, user_in)
    assert user.is_superuser == True
