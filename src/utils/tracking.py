import redis

from src.models.auth import StreetVendorCategoryEnum

def add_coordinates(rd: redis.Redis, key: str, lat: float, lon: float, name: str, vendor_category: StreetVendorCategoryEnum, vendor_id: str) -> None:
    """
    Add a new set of coordinates to the Redis database
    """
    rd.geoadd(key, (lon, lat, ";".join([str(vendor_id), str(name), str(vendor_category.name), str(vendor_category.value)])))

def remove_coordinates(rd: redis.Redis, key: str, name: str, vendor_id: str):
    return rd.zrem(key, vendor_id, name)


def get_nearby(rd: redis.Redis, key: str, lat: float, lon: float, radius: float, unit: str = "km") -> list:
    """
    Get nearby coordinates from the Redis database
    """
    return rd.georadius(key, lon, lat, radius, unit, withdist=True, withcoord=True)
