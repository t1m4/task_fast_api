from typing import Optional

from pydantic import Field, validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# Create via API
class UserCreate(UserBase):
    email: EmailStr = None
    password: str

    @validator('password')
    def password_validator(cls, v):
        if len(v) < 8:
            raise ValueError('Must contain more than 8 symbols')
        return v

# Update via API
class UserUpdate(UserBase):
    password: Optional[str] = None




class UserDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# return to the client
class UserOut(UserDBBase):
    pass

# user store in DB
class UserDB(UserBase):
    hashed_password: str
