import os
import datetime
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Serve the demo page
    return render_template("index.html")

@app.route("/collect", methods=["POST"])
def collect():
    # Get public IP via ipify (server-side)
    try:
        ip_data = requests.get("https://api.ipify.org?format=json").json()
        public_ip = ip_data.get("ip")
    except Exception:
        public_ip = "Unavailable"

    # Request headers
    ua = request.headers.get("User-Agent")
    referrer = request.headers.get("Referer")
    dnt = request.headers.get("DNT") == "1"

    # Client-side metadata sent via JS
    data = request.json or {}
    log_entry = {
        "publicIp": public_ip,
        "ua": ua,
        "referrer": referrer,
        "dnt": dnt,
        "screen": data.get("screen"),
        "tz": data.get("tz"),
        "tzOffset": data.get("tzOffset"),
        "lang": data.get("lang"),
        "cookiesEnabled": data.get("cookiesEnabled"),
        "cookiesSize": data.get("cookiesSize"),
        "platform": data.get("platform"),
        "cores": data.get("cores"),
        "memory": data.get("memory"),
        "touchPoints": data.get("touchPoints"),
        "localTime": data.get("localTime"),
        "pluginsCount": data.get("pluginsCount"),
        "vendor": data.get("vendor"),
        "gpu": data.get("gpu"),
        "battery": data.get("battery"),
        "devicesCount": data.get("devicesCount"),
        "prefersDark": data.get("prefersDark"),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # Save to info.txt
    with open("info.txt", "a") as f:
        f.write(str(log_entry) + "\n")

    return jsonify({"received": log_entry})

if __name__ == "__main__":
    # Railway sets PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
