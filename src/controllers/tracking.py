import redis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Dict, List
import json

from redis import Redis

from src.database import get_redis
from src.models.auth import StreetVendorCategoryEnum
from src.schemas.tracking import Coordinates
from src.utils.tracking import add_coordinates, get_nearby

from src.utils.auth import decode_token

router = APIRouter(prefix="/api/v1/tracking")

active_connections: Dict[str, List[WebSocket]] = {"street_vendor_room": []}


@router.websocket("/street-vendor")
async def street_vendor_websocket(websocket: WebSocket, token: str = Query(...), rd: redis.Redis = Depends(get_redis)):
    try:
        token = decode_token(token)

        if token["is_street_vendor"] is False:
            await websocket.send_text("Unauthorized")
            await websocket.close()
            return

        active_connections["street_vendor_room"].append(websocket)

        await websocket.accept()
        await websocket.send_text("Connection established")

        while True:
            try:
                data = await websocket.receive_text()
                data_json = json.loads(data)

                add_coordinates(rd, "street_vendor_locations", data_json["lat"], data_json["lon"], token["name"], token["street_vendor"]["street_vendor_category"], token["sub"])

            except WebSocketDisconnect:
                active_connections["street_vendor_room"].remove(websocket)
                break

    except Exception as e:
        await websocket.send_text(f"Error : {e.message}")
        await websocket.close()


@router.websocket("/user")
async def user_websocket(websocket: WebSocket):
    try:
        # Authorize here

        active_connections["user_room"].append(websocket)

        await websocket.accept()
        await websocket.send_text("Connection established")

    except Exception as e:
        await websocket.send_text(e.message)
        await websocket.close()


@router.get("/seed-coordinates")
async def seed_coordinates(rd: redis.Redis = Depends(get_redis)):
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9842, "Vendor 1", StreetVendorCategoryEnum.makanan_dan_minuman, 1)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.8843, "Vendor 2", StreetVendorCategoryEnum.pakaian_dan_aksesoris, 2)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9844, "Vendor 3", StreetVendorCategoryEnum.buah_dan_sayuran, 3)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9845, "Vendor 4", StreetVendorCategoryEnum.barang_bekas_dan_barang_antik, 4)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9846, "Vendor 5", StreetVendorCategoryEnum.mainan_anak_anak, 5)
    return {"message": "Coordinates seeded successfully"}


@router.post("/get-nearby")
async def get_nearby_vendors(coordinates: Coordinates, rd: Redis = Depends(get_redis)):
    return get_nearby(rd, "street_vendor_locations", coordinates.lat, coordinates.lon, 20)
