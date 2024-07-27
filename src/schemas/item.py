from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float
    street_vendor: int
    image_base64: Optional[str] = ""


class ItemUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_base64: Optional[str] = None


class ItemUpdateRequest(BaseModel):
    items: list[ItemUpdate]


class ItemCreateRequest(BaseModel):
    items: list[Item]


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    street_vendor: int

    class Config:
        orm_mode = True
