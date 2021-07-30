from typing import Optional

from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# Create via API
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Update via API
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserOut(UserBase):
    id: Optional[int] = None


class UserDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# user store in DB
class UserDB(UserBase):
    password: str
