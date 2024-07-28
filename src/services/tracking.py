import json
from fastapi import WebSocket, WebSocketDisconnect
from ..utils.tracking import add_coordinates
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

async def street_vendor_websocket_service(websocket: WebSocket, token: dict, rd, active_connections: dict):
    try:
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

                category = StreetVendorCategoryEnum(my_dict[token["street_vendor"]["street_vendor_category"]])
                add_coordinates(rd, "street_vendor_locations", data_json["lat"], data_json["lon"], token["name"], category, token["sub"])

            except WebSocketDisconnect:
                active_connections["street_vendor_room"].remove(websocket)
                break

    except Exception as e:
        await websocket.send_text(f"Error : {e.message}")
        await websocket.close()