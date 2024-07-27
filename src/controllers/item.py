from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from src.database import get_db
from src.schemas.item import ItemCreateRequest, ItemUpdateRequest
from src.services.item import create_items_service, update_items_service, get_items_by_vendor_service, \
    delete_items_batch_service

items_router = APIRouter(prefix="/api/v1/items")


@items_router.post("/create")
def create_items(items_create_request: ItemCreateRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return create_items_service(items_create_request, db, Authorize)


@items_router.put("/update")
def update_items(items_create_request: ItemUpdateRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return update_items_service(items_create_request, db, Authorize)


@items_router.get("/get-by-vendor/{vendor_id}")
def get_items_by_vendor(vendor_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return get_items_by_vendor_service(vendor_id, db, Authorize)


@items_router.delete("/delete")
def delete_items_batch(items: list[int], db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return delete_items_batch_service(items, db, Authorize)
