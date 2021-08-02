from typing import Generator, Dict

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from db.base_classes import Base
from main import app
from task_fast_api.config import settings
from tests.utils import get_token_headers

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_TEST_URI)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


item_data = {
    "title": "test_title",
    "description": "test_description",
}


@pytest.fixture(scope="module")
def user_token_headers(db: Session, client: TestClient):
    return get_token_headers(db, client)


def create_item(data, client, headers):
    url = app.url_path_for('create_item')
    data = data.copy()
    r = client.post(url, json=data, headers=headers)
    assert r.status_code == 201
    return r


def test_create_item(client: TestClient, user_token_headers: Dict):
    url = app.url_path_for('create_item')
    r = client.post(url, json=item_data, headers=user_token_headers)
    content = r.json()
    assert content.get('title') == item_data['title']
    assert content.get('description') == item_data['description']
    assert content.get('id')
    assert r.status_code == 201


def test_cannot_create_item_without_title(client: TestClient, user_token_headers: Dict):
    url = app.url_path_for('create_item')
    data = item_data.copy()
    del data['title']
    r = client.post(url, json=data, headers=user_token_headers)
    content = r.json()
    assert r.status_code == 422


def test_cannot_create_item_without_auth(client: TestClient, user_token_headers: Dict):
    url = app.url_path_for('create_item')
    r = client.post(url, json=item_data)
    assert r.status_code == 401


def test_update_item(client: TestClient, user_token_headers: Dict):
    # create item
    r = create_item(item_data, client, user_token_headers)

    # update item
    data = item_data.copy()
    del data['title']
    new_description = 'new_description'
    data['description'] = new_description
    put_url = app.url_path_for('update_item', id=r.json().get('id'))
    r = client.put(put_url, json=data, headers=user_token_headers)
    content = r.json()
    assert r.status_code == 200
    assert content.get('description') == new_description


def test_cannot_update_without_auth(client: TestClient, user_token_headers: Dict):
    put_url = app.url_path_for('update_item', id=1)
    r = client.put(put_url, json=item_data)
    assert r.status_code == 401


def test_cannot_get_without_auth(client: TestClient, user_token_headers: Dict):
    get_url = app.url_path_for('get_item', id=1)
    r = client.get(get_url, json=item_data)
    assert r.status_code == 401


def test_cannot_delete_without_auth(client: TestClient, user_token_headers: Dict):
    delete_url = app.url_path_for('delete_item', id=1)
    r = client.delete(delete_url, json=item_data)
    assert r.status_code == 401


def test_delete(client: TestClient, user_token_headers: Dict):
    r = create_item(item_data, client, user_token_headers)

    # update item
    url = app.url_path_for('delete_item', id=r.json().get('id'))
    r = client.delete(url, headers=user_token_headers)
    assert r.status_code == 200
