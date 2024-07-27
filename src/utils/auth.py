from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import jwt
from jwt.exceptions import InvalidTokenError
from ..models.auth import User, StreetVendor
from ..schemas.auth import UserLogin, UserCreate
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
    user = get_user_by_email(user.email, db)
    if user.is_street_vendor:
        street_vendor = get_street_vendor_by_id(user.id, db)
        return Authorize.create_access_token(subject=street_vendor.user, user_claims={
            "is_street_vendor": user.is_street_vendor,
            "name": user.name,
            "street_vendor": {
                "street_vendor_name": street_vendor.street_vendor_name,
                "street_vendor_category": street_vendor.street_vendor_category.name
            }
        })
    return Authorize.create_access_token(subject=user.id, user_claims={
        "is_street_vendor": user.is_street_vendor,
        "name": user.name,
    })


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return "Invalid token"
    
def create_user(user: UserCreate, db: Session):
    user_instance = User(**user.dict())
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance


def get_user(id: str, db: Session):
    return db.query(User).filter(User.id == id).first()

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_street_vendor_by_id(user: str, db: Session):
    return db.query(StreetVendor).filter(StreetVendor.user == user).first()
