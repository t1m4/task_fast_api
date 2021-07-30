from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base_classes import Base
from main import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(*args, **kwargs):
    """
    Create tables without alembic
    """
    Base.metadata.create_all(bind=engine)