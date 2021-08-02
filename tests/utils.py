import random
import string

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from auth.security import get_password_hash
from db.crud.crud_user import create_user
from db.models import User
from main import app
from schemas.user import UserCreate
from task_fast_api.config import settings


def create_test_random_user(db: Session):
    username = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    user_data = {
        'username': username,
        'email': f'{username}@mail.ru',
        "password": 'password'}
    user_in = UserCreate(**user_data)
    return create_user(db, user_in)


def get_token_headers(db: Session, client: TestClient):
    """
    Get super user jwt token
    """
    login_data = {
        'username': settings.FIRST_SUPERUSER,
        'password': settings.FIRST_SUPERUSER_PASSWORD,
    }

    # login as user
    url = app.url_path_for('get_access_token')
    r = client.post(url, data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
