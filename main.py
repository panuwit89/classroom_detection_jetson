import uvicorn
import threading
from setup import app
import config
from computer_vision_task import run_cv_loop
import route

@app.on_event("startup")
async def startup_event():
    """
    Defines the actions to take when the FastAPI server starts up.
    """
    print("INFO:     FastAPI: Startup event triggered.")
    print("INFO:     FastAPI: Starting CV thread...")
    cv_thread = threading.Thread(
        target=run_cv_loop, # Main function
        daemon=True # Stop thread when main app stops
    )
    cv_thread.start()

if __name__ == "__main__":
    print(f"INFO:     Starting FastAPI server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    uvicorn.run(
        app,  # The app object we imported from app_setup
        host=config.SERVER_HOST,
        port=config.SERVER_PORT
    )