from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.base_classes import Base


class User(Base):
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

