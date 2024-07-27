from pydantic import BaseModel, EmailStr
from typing import Optional

from src.models.auth import StreetVendorCategoryEnum


class UserBase(BaseModel):
    email: EmailStr
    is_street_vendor: Optional[bool] = False


class UserCreate(UserBase):
    name: str
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class StreetVendorBase(UserBase):
    street_vendor_name: str
    street_vendor_category: StreetVendorCategoryEnum


class StreetVendorCreate(StreetVendorBase):
    name: str
    password: str


class StreetVendor(StreetVendorBase):
    user: int

    class Config:
        orm_mode = True
