import threading

# Global data store
data_store = {
    "count": 0,
    "ema": 0.0,
    "frame": None
}

# Use Lock for prevent race condition when access date_store from more than one place at the same time
data_lock = threading.Lock()