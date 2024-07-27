from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.item import Item
from src.schemas.item import ItemCreateRequest, ItemUpdateRequest


def create_items_service(items: ItemCreateRequest, db: Session):
    try:
        # Start a transaction
        with db.begin():
            for item in items.items:
                item_instance = Item(**item.dict())
                db.add(item_instance)
            db.commit()  # Commit the transaction

        return items

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction on error
        raise e  # Optionally, re-raise the exception or handle it as needed


def update_items_service(items: ItemUpdateRequest, db: Session):
    try:
        # Start a transaction
        with db.begin():
            for item in items.items:
                update_data = {k: v for k, v in item.dict().items() if v is not None}
                db.query(Item).filter(Item.id == item.id).update(update_data)
            db.commit()  # Commit the transaction

        return items

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction on error
        raise e  # Optionally, re-raise the exception or handle it as needed


def get_items_by_vendor_service(vendor_id: int, db: Session):
    return db.query(Item).filter(Item.street_vendor == vendor_id).all()


def delete_items_batch_service(items: list[int], db: Session):
    try:
        # Start a transaction
        with db.begin():
            db.query(Item).filter(Item.id.in_(items)).delete(synchronize_session=False)
            db.commit()  # Commit the transaction

        return items

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction on error
        raise e  # Optionally, re-raise the exception or handle it as needed
