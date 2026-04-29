from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # user_id (str) -> websocket
        self.active_connections: dict[str, WebSocket] = {}

    # ✅ CONNECT
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()

        user_id = str(user_id)

        # 🔥 close old connection if exists
        if user_id in self.active_connections:
            old_ws = self.active_connections[user_id]
            try:
                await old_ws.close()
            except:
                pass

        self.active_connections[user_id] = websocket

        print(f"User {user_id} connected")
        print("ACTIVE USERS:", list(self.active_connections.keys()))

    # ✅ DISCONNECT
    def disconnect(self, user_id: str):
        user_id = str(user_id)

        self.active_connections.pop(user_id, None)

        print(f"User {user_id} disconnected")
        print("ACTIVE USERS:", list(self.active_connections.keys()))

    # ✅ SEND MESSAGE
    async def send(self, user_id: str, message: str):
        user_id = str(user_id)

        print("TRY SEND →", user_id)
        print("ACTIVE USERS:", list(self.active_connections.keys()))

        ws = self.active_connections.get(user_id)

        if ws:
            print("✅ Sending message to:", user_id)
            await ws.send_text(message)
        else:
            print(f"❌ User {user_id} not connected")


manager = ConnectionManager()