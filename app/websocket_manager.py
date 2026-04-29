from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # user_id (str) -> websocket
        self.active_connections: dict[str, WebSocket] = {}

    # ✅ CONNECT
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[str(user_id)] = websocket
        print(f"User {user_id} connected")

    # ✅ DISCONNECT
    def disconnect(self, user_id: str):
        self.active_connections.pop(str(user_id), None)
        print(f"User {user_id} disconnected")

    # ✅ SEND MESSAGE
    async def send(self, user_id: str, message: str):
        ws = self.active_connections.get(str(user_id))

        if ws:
            await ws.send_text(message)
        else:
            print(f"User {user_id} not connected")


manager = ConnectionManager()