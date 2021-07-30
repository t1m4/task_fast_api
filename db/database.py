from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base_classes import Base
from task_fast_api.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, bind=engine)

def init_db(*args, **kwargs):
    """
    Create tables without alembic
    """
    Base.metadata.create_all(bind=engine)

