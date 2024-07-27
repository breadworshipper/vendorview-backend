from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.models.item import Item
from src.schemas.item import ItemCreateRequest, ItemUpdateRequest

from fastapi_jwt_auth import AuthJWT


def create_items_service(items: ItemCreateRequest, db: Session, authorize: AuthJWT):
    try:
        authorize.jwt_required()
        current_user = authorize.get_jwt_subject()
        # Start a transaction
        with db.begin():
            for item in items.items:
                item_instance = Item(**item.dict(), street_vendor_id=current_user)
                db.add(item_instance)
            db.commit()  # Commit the transaction

        return JSONResponse(status_code=201, content={"message": "Items created successfully",
                                                      "items created": [item.dict() for item in items.items]})

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction on error
        raise e  # Optionally, re-raise the exception or handle it as needed


def update_items_service(items: ItemUpdateRequest, db: Session, authorize: AuthJWT):
    try:
        authorize.jwt_required()
        # Start a transaction
        with db.begin():
            for item in items.items:
                update_data = {k: v for k, v in item.dict().items() if v is not None}
                db.query(Item).filter(Item.id == item.id).update(update_data)
            db.commit()  # Commit the transaction

        return JSONResponse(status_code=200, content={"message": "Items updated successfully",
                                                      "items updated": [item.id for item in items.items]})

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction on error
        raise e  # Optionally, re-raise the exception or handle it as needed


def get_items_by_vendor_service(vendor_id: int, db: Session, authorize: AuthJWT):
    authorize.jwt_required()
    return db.query(Item).filter(Item.street_vendor_id == vendor_id).all()


def delete_items_batch_service(items: list[int], db: Session, authorize: AuthJWT):
    try:
        authorize.jwt_required()
        # Start a transaction
        with db.begin():
            db.query(Item).filter(Item.id.in_(items)).delete(synchronize_session=False)
            db.commit()  # Commit the transaction

        return JSONResponse(status_code=200, content={"message": "Items deleted successfully",
                                                      "items deleted": items})

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction on error
        raise e  # Optionally, re-raise the exception or handle it as needed
