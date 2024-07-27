from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import jwt
from jwt.exceptions import InvalidTokenError
from ..models.auth import User
from ..schemas.auth import UserLogin
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(user: UserLogin, Authorize: AuthJWT, db: Session):
    user = get_user(user.email, db)
    return Authorize.create_access_token(subject=user.id)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return "Invalid token"


def get_user(id: str, db: Session):
    return db.query(User).filter(User.id == id).first()
