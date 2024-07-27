from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import Base
from .auth import StreetVendor

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    street_vendor = Column(ForeignKey("street_vendors.user"))
    image_base64 = Column(String)
