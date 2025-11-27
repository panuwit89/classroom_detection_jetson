from fastapi import FastAPI
from websocket_manager import ConnectionManager

# --- App & Manager Initialization ---
app = FastAPI()
manager = ConnectionManager()