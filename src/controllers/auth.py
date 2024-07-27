from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.auth import UserCreate
from src.services.auth import register_user_service

auth_router = APIRouter(prefix="/api/v1/auth")


@auth_router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(user, db)
