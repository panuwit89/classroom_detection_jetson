from fastapi import WebSocket

# WebSocket connection manager
class ConnectionManager:
    # Create class variable
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    # Append a new connection
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Remove a connection
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Send a data for every connection
    async def broadcast_json(self, data: dict):
        data_to_send = data.copy() # Create a copy of data
        data_to_send.pop("frame", None) # Delete "frame" before send data
        for connection in self.active_connections:
            await connection.send_json(data_to_send)