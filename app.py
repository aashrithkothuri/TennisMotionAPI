import flask
import numpy as np

app = flask.Flask(__name__)

@app.route("/",methods=["POST"])
def api():
    data = flask.request.get_json()

    # 10 by 3 array containing 10 xyz data points (for acceleration and gyro)
    gyro = data.get("gyro")
    acc = data.get("acc") 

    # Time data point was taken (seconds since 1970)
    timestamp = data.get("time") 

    # Checking validity of data
    valid = np.array(gyro).shape == (10,3) and np.array(acc).shape == (10,3) and timestamp.isdigit()

    # If all data is valid
    if valid:

        # Opening file, appending new line to csv, closing file
        with open("train.csv","a") as f:
            f.write(f"\n{acc},{gyro},{timestamp}")
            f.close()

        return flask.jsonify({"status":"success"})
    
    return flask.jsonify({"status":"failure","error":"data invalid"})

    
