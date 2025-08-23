# test_api.py
import requests
import numpy as np
import time
import json
from typing import Tuple

URL = "http://127.0.0.1:5000/"

def gen_arrays(shape: Tuple[int, int] = (10, 3)):
    return np.random.randint(-500, 500, size=shape).tolist()

def valid_payload():
    return {
        "gyro": gen_arrays(),
        "acc": gen_arrays(),
        "time": str(int(time.time()))  # digits-only string
    }

def bad_shape_payload():
    return {
        "gyro": gen_arrays((9, 3)),   # wrong shape
        "acc": gen_arrays(),
        "time": str(int(time.time()))
    }

def bad_time_payload():
    return {
        "gyro": gen_arrays(),
        "acc": gen_arrays(),
        "time": "not_digits"          # invalid timestamp
    }

def send(payload, label=""):
    print(f"\n=== Sending {label or 'request'} ===")
    print(json.dumps(payload)[:200] + ("..." if len(json.dumps(payload)) > 200 else ""))
    try:
        r = requests.post(URL, json=payload, timeout=5)
        print("Status:", r.status_code)
        # Print text to handle any type of response
        print("Response:", r.text.strip() or "<empty>")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    # 1) Valid request
    send(valid_payload(), "valid payload")

    # 2) Invalid: wrong array shape
    send(bad_shape_payload(), "invalid shape")

    # 3) Invalid: bad timestamp
    send(bad_time_payload(), "invalid timestamp")
