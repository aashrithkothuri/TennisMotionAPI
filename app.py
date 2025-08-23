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
    gyro = data.get("gyro")
    acc = data.get("acc")

    # Unix timestamp (seconds since 1970)
    timestamp = data.get("time")

    # Validate
    valid = (
        np.array(gyro).shape == (10, 3)
        and np.array(acc).shape == (10, 3)
        and str(timestamp).isdigit()
    )

    if valid:
        file_exists = os.path.exists("train.csv")

        # Append JSON-serialized arrays + timestamp
        with open("train.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["acc_json", "gyro_json", "timestamp"])
            writer.writerow([json.dumps(acc), json.dumps(gyro), str(timestamp)])

        return flask.jsonify({"status": "success"}), 200

    return flask.jsonify({"status": "failure", "error": "data invalid"}), 400

if __name__ == "__main__":
    app.run(debug=True)
