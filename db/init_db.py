from sqlalchemy.orm import Session

import schemas
from db.crud import crud_user
from schemas.user import UserCreate
from task_fast_api.config import settings


def init_db(db: Session) -> None:

    user = crud_user.get_user_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=f"{settings.FIRST_SUPERUSER}@mail.com",
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud_user.create_user(db, user_in)