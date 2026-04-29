from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    # ✅ connect user
    await manager.connect(user_id, websocket)
    print(f"User {user_id} connected")

    try:
        while True:
            # ✅ keep connection alive
            data = await websocket.receive_text()
            print(f"Received from {user_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected")