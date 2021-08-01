from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


# Create via API
class UserCreate(UserBase):
    email: EmailStr = None
    password: str


# Update via API
class UserUpdate(UserBase):
    password: Optional[str] = None




class UserDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserOut(UserDBBase):
    pass

# user store in DB
class UserDB(UserBase):
    hashed_password: str
