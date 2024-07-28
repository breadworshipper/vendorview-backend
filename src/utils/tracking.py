import redis

from src.models.auth import StreetVendorCategoryEnum

my_dict = {
    "makanan_dan_minuman": 1,
    "pakaian_dan_aksesoris": 2,
    "buah_dan_sayuran": 3,
    "barang_bekas_dan_barang_antik": 4,
    "mainan_anak_anak": 5,
    "jasa" : 6,
    "kerajinan_tangan" : 7,
    "produk_kesehatan_dan_kecantikan" : 8,
    "peralatan_rumah_tangga" : 9,
    "barang_elektronik" : 10
}

def add_coordinates(rd: redis.Redis, key: str, lat: float, lon: float, name: str, vendor_category: StreetVendorCategoryEnum, vendor_id: str) -> None:
    """
    Add a new set of coordinates to the Redis database
    """
    rd.geoadd(key, (lon, lat, ";".join([str(vendor_id), str(name), str(vendor_category.name), str(vendor_category.value)])))

def remove_coordinates(rd: redis.Redis, key: str, name: str, vendor_id: str, token: dict):
    category = StreetVendorCategoryEnum(my_dict[token["street_vendor"]["street_vendor_category"]])
    member = ";".join([str(vendor_id), name, category.name, str(category.value)])
    print(member)
    return rd.zrem(key, member)


def get_nearby(rd: redis.Redis, key: str, lat: float, lon: float, radius: float, unit: str = "km") -> list:
    """
    Get nearby coordinates from the Redis database
    """
    return rd.georadius(key, lon, lat, radius, unit, withdist=True, withcoord=True)
