from typing import Generator, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

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


@pytest.fixture(scope="module")
def user_token_headers(db: Session, client: TestClient):
    return get_token_headers(db, client)


def test_get_users(client: TestClient, user_token_headers: Dict):
    url = app.url_path_for('get_users')
    r = client.get(url, headers=user_token_headers)
    response = r.json()
    assert isinstance(response, list)


def test_get_user_me(client: TestClient, user_token_headers: Dict):
    url = app.url_path_for('check_current_user')
    r = client.get(url, headers=user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user.get('username')
    assert current_user.get('email')
    assert current_user.get('full_name') is None
    assert current_user.get("is_superuser")
    assert current_user.get("is_active") is True
