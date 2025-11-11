import threading
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# list of websites to check
WEBSITES = [
    "https://google.com",
    "https://example.com",
    "https://github.com",
    "https://sm-manager-ub0i.onrender.com",
    "https://aubot-1.onrender.com",
]

# store latest ping results
STATUS = {
    site: {
        "status": "Unknown",
        "code": None,
        "last_checked": None
    }
    for site in WEBSITES
}

def ping_websites():
    while True:
        print("\n=== PING START ===")
        for site in WEBSITES:
            try:
                resp = requests.get(site, timeout=10)
                STATUS[site]["status"] = "UP"
                STATUS[site]["code"] = resp.status_code
                STATUS[site]["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[UP] {site} -> {resp.status_code}")
            except Exception as e:
                STATUS[site]["status"] = "DOWN"
                STATUS[site]["code"] = None
                STATUS[site]["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[DOWN] {site} -> {str(e)}")
        print("=== WAITING 5 MINS ===\n")
        time.sleep(300)  # 5 minutes


@app.route("/")
def index():
    # return simple HTML status table
    html = "<h2>Website Status Monitor</h2><table border='1' cellpadding='5'>"
    html += "<tr><th>Website</th><th>Status</th><th>HTTP Code</th><th>Last Checked</th></tr>"

    for site, info in STATUS.items():
        color = "green" if info["status"] == "UP" else "red"
        html += f"<tr>" \
                f"<td>{site}</td>" \
                f"<td style='color:{color}'><b>{info['status']}</b></td>" \
                f"<td>{info['code']}</td>" \
                f"<td>{info['last_checked']}</td>" \
                f"</tr>"

    html += "</table>"
    return html


@app.route("/api/status")
def api_status():
    return jsonify(STATUS)


def start_background_task():
    t = threading.Thread(target=ping_websites)
    t.daemon = True
    t.start()


if __name__ == "__main__":
    start_background_task()
    app.run(host="0.0.0.0", port=5010, debug=False)
