from sqlalchemy import Column, ForeignKey, Integer, String, Float

from ..database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    street_vendor = Column(ForeignKey("street_vendors.user"))
