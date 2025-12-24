SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

MODEL_PATH = "yolo11n.engine"
VIDEO_SOURCE = 0  # Used Webcam
CLASSES_TO_DETECT = [0, 56]  # 0: person, 56: chair
TRACKER_CONFIG_PATH = "bytetrack_custom.yaml" # Custom Bytetrack Setting

DETECTOR_CONF_THRESHOLD = 0.1 # The Minimum conf sending to Bytetrack model
PATIENCE_SECONDS = 3      # Keep object id for this patience time
SMOOTHING_FACTOR = 0.05    # for Exponential Moving Average (EMA)

DEVICE_ID = "room_101"
MQTT_BROKER_IP = "172.20.10.7" # IP Laptop (Server IP)
MQTT_PORT = 1883
