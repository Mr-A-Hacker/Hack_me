import os
import datetime
import requests
import socket
import platform
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Public IP via ipify
        try:
            ip_data = requests.get("https://api.ipify.org?format=json").json()
            public_ip = ip_data.get("ip")
        except Exception:
            public_ip = "Unavailable"

        # Client IP from Flask
        client_ip = request.remote_addr

        # Request metadata
        ua = request.headers.get("User-Agent")
        referrer = request.headers.get("Referer")
        dnt = request.headers.get("DNT") == "1"
        headers = dict(request.headers)

        # Client-side metadata sent via JS
        data = request.get_json(force=True) or {}

        # Reverse DNS lookup
        try:
            reverse_dns = socket.getfqdn(client_ip)
        except Exception:
            reverse_dns = "Unavailable"

        # Server environment info
        server_info = {
            "serverHost": socket.gethostname(),
            "serverOS": platform.system() + " " + platform.release(),
            "pythonVersion": platform.python_version()
        }

        log_entry = {
            "publicIp": public_ip,
            "clientIp": client_ip,
            "reverseDns": reverse_dns,
            "ua": ua,
            "referrer": referrer,
            "dnt": dnt,
            "headers": headers,
            "screen": data.get("screen"),
            "tz": data.get("tz"),
            "lang": data.get("lang"),
            "cookiesEnabled": data.get("cookiesEnabled"),
            "platform": data.get("platform"),
            "userAgent": data.get("userAgent"),
            "online": data.get("online"),
            "cores": data.get("cores"),
            "ramGB": data.get("ramGB"),
            "touchPoints": data.get("touchPoints"),
            "vendor": data.get("vendor"),
            "productSub": data.get("productSub"),
            "pixelRatio": data.get("pixelRatio"),
            "plugins": data.get("plugins"),
            "connection": data.get("connection"),
            "battery": data.get("battery"),
            "storage": data.get("storage"),
            "location": data.get("location"),
            "timestampUTC": datetime.datetime.utcnow().isoformat(),
            "timestampLocal": datetime.datetime.now().isoformat(),
            "epochTime": datetime.datetime.now().timestamp(),
            "serverInfo": server_info
        }

        # Save to info.txt
        with open("info.txt", "a") as f:
            f.write(str(log_entry) + "\n")

        return jsonify({"received": log_entry})

    # GET request → serve the demo page
    return render_template("index.html")

# Secure logs route
@app.route("/logs")
def logs():
    try:
        with open("info.txt", "r") as f:
            return "<pre>" + f.read() + "</pre>"
    except FileNotFoundError:
        return "No logs yet."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
