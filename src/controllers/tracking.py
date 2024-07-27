import redis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json

from redis import Redis

from src.database import get_redis
from src.models.auth import StreetVendorCategoryEnum
from src.schemas.tracking import Coordinates
from src.utils.tracking import add_coordinates, get_nearby

router = APIRouter(prefix="/api/v1/tracking")

active_connections: Dict[str, List[WebSocket]] = {"street_vendor_room": [], "user_room": []}


@router.websocket("/street-vendor")
async def street_vendor_websocket(websocket: WebSocket):
    try:
        # Authorize here

        active_connections["street_vendor_room"].append(websocket)

        await websocket.accept()
        await websocket.send_text("Connection established")

        while True:
            try:
                data = await websocket.receive_text()
                message_data = {
                    "data": data,
                    "street_vendor_id": 1
                }
                json_message = json.dumps(message_data)

                print(active_connections)
                if len(active_connections["user_room"]) != 0:
                    for connection in active_connections["user_room"]:
                        await connection.send_text(json_message)

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
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9842, "Vendor 1", StreetVendorCategoryEnum.makanan_dan_minuman)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9843, "Vendor 2", StreetVendorCategoryEnum.pakaian_dan_aksesoris)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9844, "Vendor 3", StreetVendorCategoryEnum.buah_dan_sayuran)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9845, "Vendor 4", StreetVendorCategoryEnum.barang_bekas_dan_barang_antik)
    add_coordinates(rd, "street_vendor_locations", 14.5995, 120.9846, "Vendor 5", StreetVendorCategoryEnum.mainan_anak_anak)
    return {"message": "Coordinates seeded successfully"}


@router.post("/get-nearby")
async def get_nearby_vendors(coordinates: Coordinates, rd: Redis = Depends(get_redis)):
    return get_nearby(rd, "street_vendor_locations", coordinates.lat, coordinates.lon, 20)
