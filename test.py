# test.py  
# (completely AI generated)
# "pytest test.py" to run tests (optionally -vv and/or -rA for a summary and explanation)

import csv
import json
import sys
import importlib
from pathlib import Path
import pytest

def make_10x3(start=0):
    # [[0,1,2], [3,4,5], ...] -> 10 rows
    return [[i, i+1, i+2] for i in range(start, start + 30, 3)]

def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.reader(f))

@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    Inline fixture so you only need this one test file.
    Assumes your Flask code lives in app.py and exposes `app`.
    """
    # Write CSVs into a temp dir so tests don't touch real files
    monkeypatch.chdir(tmp_path)

    # Fresh import of the Flask app module
    if "app" in sys.modules:
        del sys.modules["app"]
    app_module = importlib.import_module("app")
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as c:
        yield c

def test_sensor_payload_writes_csv_and_returns_200(client):
    acc = make_10x3(0)
    gyro = make_10x3(100)
    ts = 1699999999.5  # float timestamp is allowed by your code

    r = client.post("/", json={"acc": acc, "gyro": gyro, "time": ts})
    assert r.status_code == 200
    assert r.get_json()["status"] == "success"

    p = Path("motionsensors.csv")
    assert p.exists()
    rows = read_csv(p)
    assert rows[0] == ["acc_json", "gyro_json", "timestamp"]  # header
    assert rows[1][0] == json.dumps(acc)
    assert rows[1][1] == json.dumps(gyro)
    assert rows[1][2] == str(ts)

def test_speed_payload_writes_csv_and_returns_200(client):
    speed = 35      # ints only pass your current str(...).isdigit() check
    ts = 1700000000

    r = client.post("/", json={"speed": speed, "time": ts})
    assert r.status_code == 200
    assert r.get_json()["status"] == "success"

    p = Path("speedsensor.csv")
    assert p.exists()
    rows = read_csv(p)
    assert rows[0] == ["speed", "timestamp"]  # header
    # your code uses json.dumps(speed) -> "35"
    assert rows[1] == [json.dumps(speed), str(ts)]

def test_both_payloads_present_prefers_sensor_branch(client):
    acc = make_10x3(0)
    gyro = make_10x3(100)
    ts = 1700000001
    speed = 42

    r = client.post("/", json={"acc": acc, "gyro": gyro, "time": ts, "speed": speed})
    assert r.status_code == 200
    assert Path("motionsensors.csv").exists()
    # speed file should not be created because of the `elif`
    assert not Path("speedsensor.csv").exists()

def test_invalid_payload_returns_400(client):
    r = client.post("/", json={})
    assert r.status_code == 400
    body = r.get_json()
    assert body["status"] == "failure"
    assert "invalid" in body["error"]

def test_speed_float_is_rejected_by_isdigit(client):
    # Documents current behavior: floats don't pass str(...).isdigit()
    r = client.post("/", json={"speed": 12.34, "time": 1700000002})
    assert r.status_code == 400
    assert r.get_json()["status"] == "failure"
