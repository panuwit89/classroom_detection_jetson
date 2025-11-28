import cv2
import json
from ultralytics import YOLO
import paho.mqtt.client as mqtt
import config
from global_state import data_store, data_lock

# --- MQTT Setup ---
mqtt_client = mqtt.Client()
mqtt_topic = f"classroom/{config.DEVICE_ID}/data" # แยก topic ตาม ID ของ Jetson

def run_cv_loop():
    """
    Function running in Thread for video processing
    
    Args:
        manager (ConnectionManager): Instacne of Manager use for broadcast
        main_loop (asyncio.AbstractEventLoop): Event loop of FastAPI
    """
    try:
        mqtt_client.connect(config.MQTT_BROKER_IP, config.MQTT_PORT, 60)
        mqtt_client.loop_start() # รัน background thread สำหรับ MQTT
        print(f"INFO:     MQTT Connected to {config.MQTT_BROKER_IP}")
    except Exception as e:
        print(f"ERROR:    MQTT Connection failed: {e}")

    print("INFO:     CV Thread: Initializing model...")
    model = YOLO(config.MODEL_PATH, task='detect')
    cap = cv2.VideoCapture(config.VIDEO_SOURCE)

    if not cap.isOpened():
        print(f"INFO:     CV Thread: Error opening video source {config.VIDEO_SOURCE}")
        return

    frame_idx, stable_count, stable_count_ema, smoothing = 0, 0, 0.0, config.SMOOTHING_FACTOR

    print("INFO:     CV Thread: Starting loop...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("INFO:     CV Thread: Cannot read a frame from camera. Exiting.")
            break

        # --- Model Tracking ---
        results = model.track(
            source=frame,
            persist=True,
            classes=config.CLASSES_TO_DETECT,
            device=0,
            conf=config.DETECTOR_CONF_THRESHOLD,
            tracker=config.TRACKER_CONFIG_PATH,
            agnostic_nms=False,
            verbose=False,
        )

        boxes = results[0].boxes

        if boxes.id is not None:
            stable_count = len(boxes.id)
        else:
            stable_count = 0

        stable_count_ema = smoothing * stable_count + (1 - smoothing) * stable_count_ema

        annotated_frame = results[0].plot()

        # --- Encode Frame ---
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            print("INFO:     CV Thread: Failed to encode frame.")
            continue
        
        frame_bytes = buffer.tobytes()

        with data_lock:
            data_store["count"] = stable_count
            data_store["ema"] = round(stable_count_ema, 2)
            data_store["frame"] = frame_bytes
        
        # --- MQTT Publish (ส่วนที่เปลี่ยนใหม่) ---
        payload = {
            "device_id": config.DEVICE_ID,
            "count": stable_count,
            "ema": round(stable_count_ema, 2)
        }

        if frame_idx % 30 == 0: 
            mqtt_client.publish(mqtt_topic, json.dumps(payload))

        frame_idx += 1

    print("INFO:     CV Thread: Releasing resources.")
    cap.release()