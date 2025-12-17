import asyncio
from fastapi.responses import StreamingResponse
from setup import app
from global_state import data_store, data_lock

@app.get("/video_feed")
async def video_feed():
    """Endpoint for the MJPEG video stream."""
    
    async def frame_generator():
        while True:
            with data_lock:
                frame_bytes = data_store.get("frame")
            
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Control frame rate
            await asyncio.sleep(1/30)

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")