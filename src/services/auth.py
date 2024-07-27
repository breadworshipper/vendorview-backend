from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.models.auth import User, StreetVendor
from src.schemas.auth import UserCreate, UserLogin, StreetVendorCreate
from src.utils.auth import hash_password, create_access_token, verify_password, get_user_by_email, create_user


def register_user_service(user: UserCreate, db: Session):
    if get_user_by_email(user.email, db):
        return JSONResponse(status_code=409, content={"message": "User already exists"})

    user_instance = create_user(user, db)

    # TODO: Make a DTO for the response
    return JSONResponse(status_code=201, content={"id": user_instance.id, "email": user_instance.email})


def register_vendor_service(street_vendor: StreetVendorCreate, db: Session):
    try:
        if get_user_by_email(street_vendor.email, db):
            return JSONResponse(status_code=409, content={"message": "User already exists"})

        # Start a transaction
        with db.begin_nested():
            user_instance = User(email=street_vendor.email, name=street_vendor.name,
                                 password=hash_password(street_vendor.password), is_street_vendor=True)
            db.add(user_instance)
            db.flush()  # Ensure user_instance.id is available

            street_vendor_instance = StreetVendor(street_vendor_name=street_vendor.street_vendor_name,
                                                  street_vendor_category=street_vendor.street_vendor_category,
                                                  user=user_instance.id)
            db.add(street_vendor_instance)
            db.flush()

        db.commit()

        return JSONResponse(status_code=201, content={"id": user_instance.id,
                                                      "email": user_instance.email,
                                                      "street_vendor": {
                                                          "street_vendor_name": street_vendor_instance.street_vendor_name,
                                                          "street_vendor_category": street_vendor_instance.street_vendor_category.name
                                                      }
                                                      })

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": str(e)})


def login_user_service(user: UserLogin, db: Session, authorize: AuthJWT):
    user_instance = get_user_by_email(user.email, db)
    if user_instance and verify_password(user.password, user_instance.password):
        return JSONResponse(status_code=200, content={"access_token": create_access_token(user, authorize, db)})
    else:
        return JSONResponse(status_code=401, content={"message": "Bad credentials"})
