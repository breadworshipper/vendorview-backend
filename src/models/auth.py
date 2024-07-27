from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from ..database import Base
import enum

class StreetVendorCategoryEnum(enum.Enum):
    makanan_dan_minuman = 1
    pakaian_dan_aksesoris = 2
    buah_dan_sayuran = 3
    barang_bekas_dan_barang_antik = 4
    mainan_anak_anak = 5
    jasa = 6
    kerajinan_tangan = 7
    produk_kesehatan_dan_kecantikan = 8
    peralatan_rumah_tangga = 9
    barang_elektronik = 10

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_street_vendor = Column(Boolean, default=False, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

class StreetVendor(Base):
    __tablename__ = "street_vendors"
    
    user = Column(ForeignKey("users.id"), primary_key=True)
    street_vendor_name = Column(String)
    stree_vendor_category = Column(SQLAlchemyEnum(StreetVendorCategoryEnum, name="street_vendor_category_enum"))
