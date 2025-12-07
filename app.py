from flask import Flask, request, jsonify, render_template
import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/collect", methods=["POST"])
def collect():
    # Get public IP via ipify (server-side)
    try:
        ip_data = requests.get("https://api.ipify.org?format=json").json()
        public_ip = ip_data.get("ip")
    except Exception:
        public_ip = "Unavailable"

    ua = request.headers.get("User-Agent")
    referrer = request.headers.get("Referer")
    dnt = request.headers.get("DNT") == "1"

    data = request.json or {}
    log_entry = {
        "publicIp": public_ip,
        "ua": ua,
        "referrer": referrer,
        "dnt": dnt,
        "screen": data.get("screen"),
        "tz": data.get("tz"),
        "lang": data.get("lang"),
        "cookiesEnabled": data.get("cookiesEnabled"),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # Save to info.txt
    with open("info.txt", "a") as f:
        f.write(str(log_entry) + "\n")

    return jsonify({"received": log_entry})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
