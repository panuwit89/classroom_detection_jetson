import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

# Import global instances from other files
from setup import app, manager
from global_state import data_store, data_lock

# --- Mount Static Files ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- HTTP Endpoints ---
@app.get("/")
async def get_index():
    """Serves the main index.html file."""
    return FileResponse("static/index.html")

@app.get("/video_feed")
async def video_feed():
    """Endpoint for the MJPEG video stream."""
    
    async def frame_generator():
        """Generator that yields frames from the shared data_store."""
        while True:
            with data_lock:
                frame_bytes = data_store.get("frame")
            
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Control frame rate
            await asyncio.sleep(1/30)

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

# --- WebSocket Endpoint ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint for WebSocket connections to broadcast count/EMA data."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive, waiting for a disconnect
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)