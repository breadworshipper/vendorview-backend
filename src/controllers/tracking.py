from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

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



        