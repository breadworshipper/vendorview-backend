from sqlalchemy.orm import Session

from src.models.auth import User
from src.schemas.auth import UserCreate
from src.utils.auth import hash_password


def register_user_service(user: UserCreate, db: Session) -> User:
    user_instance = User(**user.dict())
    user_instance.password = hash_password(user_instance.password)
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance
