from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.item import Item
from src.schemas.item import ItemCreateRequest


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
