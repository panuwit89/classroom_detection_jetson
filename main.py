import uvicorn
import asyncio
import threading

# Import the app and manager from our setup file
from setup import app, manager

# Import config for host/port and the cv_loop function
import config
from computer_vision_task import run_cv_loop

# --- IMPORTANT ---
# Import the routes file. Python will execute the file,
# which registers all the @app.get/websocket decorators.
import route

# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    """
    Defines the actions to take when the FastAPI server starts up.
    This will start the separate Computer Vision thread.
    """
    print("INFO:     FastAPI: Startup event triggered.")
    
    # Get the main asyncio event loop
    main_loop = asyncio.get_running_loop()
    
    # Start the CV thread
    print("INFO:     FastAPI: Starting CV thread...")
    cv_thread = threading.Thread(
        target=run_cv_loop,        # Function to run
        args=(manager, main_loop), # Arguments for the function
        daemon=True                # Stop thread when main app stops
    )
    cv_thread.start()

# --- Main Execution ---
if __name__ == "__main__":
    print(f"INFO:     Starting FastAPI server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    uvicorn.run(
        app,  # The app object we imported from app_setup
        host=config.SERVER_HOST,
        port=config.SERVER_PORT
    )