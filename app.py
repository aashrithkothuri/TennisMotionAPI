import flask
import numpy as np
import csv
import json
import os

app = flask.Flask(__name__)

@app.route("/", methods=["POST"])
def api():
    data = flask.request.get_json()

    # 10x3 arrays
    gyro = data.get("gyro", None) # Gyroscope data
    acc = data.get("acc", None) # Accelerometer data

    # Int
    speed = data.get("speed", None) # Speed data (mph)

    # Unix timestamp (seconds since 1970)
    timestamp = data.get("time", None)

    # Checking which type of payload (sensor data or speed data) and validity
    validSensorPayload = (
        np.array(gyro).shape == (10, 3)
        and np.array(acc).shape == (10, 3)
        and isinstance(timestamp,(float,int))
    )
    validSpeedPayload = (
        str(speed).isdigit()
        and isinstance(timestamp,(float,int))
    )

    # Writing data to sensors csv 
    if validSensorPayload:
        file_exists = os.path.exists("motionsensors.csv")

        # Append JSON-serialized data + timestamp
        with open("motionsensors.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["acc_json", "gyro_json", "timestamp"])
            writer.writerow([json.dumps(acc), json.dumps(gyro), str(timestamp)])

        return flask.jsonify({"status": "success"}), 200
    
    # Writing data to speed csv
    elif validSpeedPayload: # elif instead of if to prevent speed and sensor data being added at the same time
        file_exists = os.path.exists("speedsensor.csv")

        # Append JSON-serialized data + timestamp
        with open("speedsensor.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["speed", "timestamp"])
            writer.writerow([json.dumps(speed), str(timestamp)])

        return flask.jsonify({"status": "success"}), 200

    return flask.jsonify({"status": "failure", "error": "data invalid"}), 400

if __name__ == "__main__":
    app.run(debug=True)
