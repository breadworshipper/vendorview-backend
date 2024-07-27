from typing import Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
    lat: float
    lon: float
    name: Optional[str] = ""
