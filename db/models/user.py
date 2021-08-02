from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from db.base_classes import Base


class User(Base):
    full_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    items = relationship("Item", back_populates="owner")
