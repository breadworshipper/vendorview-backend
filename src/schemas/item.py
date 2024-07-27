from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float
    street_vendor: int


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
