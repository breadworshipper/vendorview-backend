from typing import Any

from fastapi.responses import JSONResponse, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.models.auth import User
from src.schemas.auth import UserCreate, UserLogin, StreetVendorCreate
from src.utils.auth import hash_password, create_access_token, verify_password, get_user, get_user_by_email


def register_user_service(user: UserCreate, db: Session) -> Response:
    if get_user_by_email(user.email, db):
        return JSONResponse(status_code=409, content={"message": "User already exists"})
    user_instance = User(**user.dict())
    user_instance.password = hash_password(user_instance.password)
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    # TODO: Make a DTO for the response
    return JSONResponse(status_code=201, content={"id": user_instance.id, "email": user_instance.email})


def register_vendor_service(vendor: StreetVendorCreate, db: Session) -> Response:
    if get_user_by_email(vendor.email, db):
        return JSONResponse(status_code=409, content={"message": "User already exists"})
    user_attributes = vendor.dict(exclude={"street_vendor_name", "street_vendor_category"})
    return JSONResponse(status_code=201, content={"message": user_attributes})


def login_user_service(user: UserLogin, db: Session, authorize: AuthJWT) -> JSONResponse | Any:
    user_instance = get_user_by_email(user.email, db)
    if user_instance and verify_password(user.password, user_instance.password):
        return JSONResponse(status_code=200, content={"access_token": create_access_token(user, authorize, db)})
    else:
        return JSONResponse(status_code=401, content={"message": "Bad credentials"})
