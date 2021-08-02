import logging
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.base_classes import Base
from db.crud.crud_item import create_item, get_item, update_item, delete_item
from db.crud.crud_user import create_user
from db.models import User
from schemas.item import ItemCreate, ItemUpdate
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


def delete_user(db, user):
    db.delete(user)
    db.commit()

item_data = {
    'title': 'hello',
    # 'description': 'world',
}


def create_test_user(db: Session):
    user_data = {'username': 'username', 'email': 'email@mail.ru', "password": 'password'}
    user_in = UserCreate(**user_data)
    user = create_user(db, user_in)
    return user


# def test_create_item(db: Session):
#     item_in = ItemCreate(**item_data)
#     user = create_test_user(db)
#     item = create_item(db, item_in, owner_id=user.id)

def test_get_item(db: Session):
    item = get_item(db, 1)


def test_update_item(db: Session):
    item = get_item(db, 1)
    update_item(db, item, ItemUpdate(title="title2", description="description2", owner_id=2))

def test_delete_item(db: Session):
    item = get_item(db, 1)
    delete_item(db, item)