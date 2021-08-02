from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db.models import Item
from schemas.item import ItemCreate, ItemDB, ItemUpdate


def get_item(db: Session, id: int):
    return db.query(Item).filter(Item.id == id).first()


def get_all_owner_items(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(Item).filter(Item.owner_id == owner_id).offset(skip).limit(limit).all()


def create_item(db: Session, item_in: ItemCreate, owner_id: int):
    db_item = ItemDB(**item_in.dict(), owner_id=owner_id)
    item = Item(**db_item.dict(), owner_id=owner_id)
    db.add(item)
    db.commit()
    return item


def update_item(db: Session, item_db: Item, item_in: ItemUpdate):
    """
    Update db_item each attribute if attribute in item_in
    """
    item_data = jsonable_encoder(item_db)
    update_data = item_in.dict(exclude_unset=True)
    for field in item_data:
        if field in update_data:
            setattr(item_db, field, update_data[field])
    db.commit()
    return item_db


def delete_item(db: Session, item_db: Item):
    db.delete(item_db)
    db.commit()
    return item_db
