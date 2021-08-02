from fastapi import HTTPException

from db.models import Item


def check_user_have_item(item: Item, user_id):
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
