import json
from fastapi import WebSocket, WebSocketDisconnect
from ..utils.tracking import add_coordinates

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

                add_coordinates(rd, "street_vendor_locations", data_json["lat"], data_json["lon"], token["name"], token["street_vendor"]["street_vendor_category"], token["sub"])

            except WebSocketDisconnect:
                active_connections["street_vendor_room"].remove(websocket)
                break

    except Exception as e:
        await websocket.send_text(f"Error : {e.message}")
        await websocket.close()