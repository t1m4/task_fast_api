from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from api.dependencies import get_db, get_current_user
from api.utils import check_user_have_item
from db.crud import crud_item
from db.models import User
from schemas.item import ItemOut, ItemCreate, ItemUpdate

router = APIRouter()


@router.get('/', response_model=List[ItemOut])
def get_items(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=0, le=100),
        current_user: User = Depends(get_current_user)
):
    return crud_item.get_all_owner_items(db, current_user.id, skip=skip, limit=limit)


@router.post('', response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(
        *,
        db: Session = Depends(get_db),
        item_in: ItemCreate,
        current_user: User = Depends(get_current_user)
):
    return crud_item.create_item(db, item_in, current_user.id)


@router.put('/{id}', response_model=ItemOut)
def update_item(
        *,
        db: Session = Depends(get_db),
        id: int,
        item_in: ItemUpdate,
        current_user: User = Depends(get_current_user)
):
    item = crud_item.get_item(db, id)
    check_user_have_item(item, current_user.id)
    return crud_item.update_item(db, item, item_in)


@router.delete('/{id}', response_model=ItemOut)
def delete_item(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: User = Depends(get_current_user)
):
    item = crud_item.get_item(db, id)
    check_user_have_item(item, current_user.id)
    return crud_item.delete_item(db, item)


@router.get('/{id}', response_model=ItemOut)
def get_item(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: User = Depends(get_current_user)
):
    item = crud_item.get_item(db, id)
    check_user_have_item(item, current_user.id)
    return item
