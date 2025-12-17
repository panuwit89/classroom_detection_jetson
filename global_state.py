import threading

data_store = {
    "frame": None
}

# Use Lock for prevent race condition when access date_store from more than one place at the same time
data_lock = threading.Lock()