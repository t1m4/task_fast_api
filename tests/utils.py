import random
import string

from sqlalchemy.orm import Session

from db.crud.crud_user import create_user
from schemas.user import UserCreate


def create_test_random_user(db: Session):
    username = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    user_data = {
        'username': username,
        'email': f'{username}@mail.ru',
        "password": 'password'}
    user_in = UserCreate(**user_data)
    return create_user(db, user_in)
