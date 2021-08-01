import logging
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


@pytest.fixture()
def email():
    return "test@gmail.com"


@pytest.fixture()
def password():
    return "testtest"


def delete_user(db, user):
    db.delete(user)
    db.commit()


def test_create_user(db: Session, email, password):
    user_in = UserCreate(email=email, password=password)
    user = create_user(db, user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
    delete_user(db, user)


def test_create_user_active(db: Session, email, password):
    user_in = UserCreate(email=email, password=password, is_active=True)
    user = create_user(db, user_in)
    assert user.is_active == True
    delete_user(db, user)
