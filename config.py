# --- Server Settings ---
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# --- CV Model Settings ---
MODEL_PATH = "yolo11n.engine"
VIDEO_SOURCE = 0  # Used Webcam
CLASSES_TO_DETECT = [0, 56]  # 0: person, 56: chair
TRACKER_CONFIG_PATH = "bytetrack_custom.yaml" # Custom Bytetrack Setting

# --- Tracking Parameters ---
DETECTOR_CONF_THRESHOLD = 0.1 # The Minimum conf sending to Bytetrack model
PATIENCE_SECONDS = 3      # Keep object id for this patience time
SMOOTHING_FACTOR = 0.05    # for Exponential Moving Average (EMA)

DEVICE_ID = "room_101" # แต่ละเครื่องต้องตั้งชื่อไม่ซ้ำกัน
MQTT_BROKER_IP = "10.32.49.248" # IP ของเครื่อง Server กลาง
MQTT_PORT = 1883