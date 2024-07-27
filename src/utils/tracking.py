import redis


def add_coordinates(rd: redis.Redis, key: str, lat: float, lon: float, name: str) -> None:
    """
    Add a new set of coordinates to the Redis database
    """
    rd.geoadd(key, (lon, lat, name))


def get_nearby(rd: redis.Redis, key: str, lat: float, lon: float, radius: float, unit: str = "km") -> list:
    """
    Get nearby coordinates from the Redis database
    """
    return rd.georadius(key, lon, lat, radius, unit, withdist=True, withcoord=True)
