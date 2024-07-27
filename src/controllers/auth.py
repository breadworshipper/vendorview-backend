from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.auth import UserCreate, UserLogin
from src.services.auth import register_user_service, login_user_service

auth_router = APIRouter(prefix="/api/v1/auth")


@auth_router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(user, db)


@auth_router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    return login_user_service(user, db, authorize)
