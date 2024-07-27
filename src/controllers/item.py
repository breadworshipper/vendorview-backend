from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.item import ItemCreateRequest, ItemUpdateRequest
from src.services.item import create_items_service, update_items_service

items_router = APIRouter(prefix="/api/v1/items")


@items_router.post("/create")
def create_items(items_create_request: ItemCreateRequest, db: Session = Depends(get_db)):
    return create_items_service(items_create_request, db)


@items_router.put("/update")
def update_items(items_create_request: ItemUpdateRequest, db: Session = Depends(get_db)):
    return update_items_service(items_create_request, db)
