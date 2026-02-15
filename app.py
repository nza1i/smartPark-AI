from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os

app = Flask(__name__)
CORS(app)

parking = {"SPOT_01": {"status": 0, "entry": 0}}
LIMIT = 20  # 20 seconds demo overstay

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    slot = data["node_id"]
    status = data["status"]

    if status == 1 and parking[slot]["status"] == 0:
        parking[slot]["entry"] = time.time()

    parking[slot]["status"] = status
    return jsonify({"msg": "updated"})

@app.route("/")
def dashboard():
    output = ""
    for slot, info in parking.items():
        if info["status"] == 1:
            timer = int(time.time() - info["entry"])
            violation = timer > LIMIT
            output += f"{slot}: OCCUPIED | {timer}s "
            if violation:
                output += "🚨 OVERSTAY\n"
            else:
                output += "\n"
        else:
            output += f"{slot}: AVAILABLE\n"
    return "<pre>" + output + "</pre>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
