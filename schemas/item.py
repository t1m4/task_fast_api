from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Create via API
class ItemCreate(ItemBase):
    title: str

# Update via API
class ItemUpdate(ItemBase):
    pass

class ItemDBBase(ItemBase):
    id: int
    title: str

    class Config:
        orm_mode = True

# return to the client
class ItemOut(ItemDBBase):
    pass

# item store in db
class ItemDB(ItemBase):
    pass