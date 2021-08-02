from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.base_classes import Base
from db.crud.crud_item import create_item, get_item, update_item
from schemas.item import ItemCreate, ItemUpdate
from task_fast_api.config import settings
# create test db
from tests.utils import create_test_random_user

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
    'description': 'world',
}
update_item_data = {
    'title': 'hello1',
    'description': 'world1',
}


def test_create_item(db: Session):
    user = create_test_random_user(db)
    item_in = ItemCreate(**item_data)
    item = create_item(db, item_in, owner_id=user.id)
    assert item.title == item_data['title']
    assert item.description == item_data['description']


def test_get_not_exist_item(db: Session):
    item = get_item(db, 100)
    assert item is None


def test_update_item(db: Session):
    user = create_test_random_user(db)
    item_in = ItemCreate(**item_data)
    item = create_item(db, item_in, owner_id=user.id)

    item = get_item(db, item.id)
    new_item = update_item(db, item, ItemUpdate(**update_item_data))
    assert new_item.title == update_item_data['title']
    assert new_item.description == update_item_data['description']
