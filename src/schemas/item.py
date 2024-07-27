from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float
    street_vendor: int
    image_base64: Optional[str] = ""


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
