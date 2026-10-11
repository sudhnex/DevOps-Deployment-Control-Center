from flask import Flask, jsonify, render_template
from datetime import datetime, timezone

app = Flask(__name__)
START_TIME = datetime.now(timezone.utc)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "deployment-control-center"
    }), 200


@app.route("/api/status")
def status():
    return jsonify({
        "application": "online",
        "environment": "development",
        "uptime_seconds": int(
            (datetime.now(timezone.utc) - START_TIME).total_seconds()
        ),
        "checked_at": datetime.now(timezone.utc).isoformat()
    })


@app.route("/api/deployments")
def deployments():
    return jsonify([
        {
            "id": "DEP-001",
            "service": "frontend",
            "status": "SUCCESS",
            "environment": "development"
        },
        {
            "id": "DEP-002",
            "service": "backend-api",
            "status": "SUCCESS",
            "environment": "development"
        },
        {
            "id": "DEP-003",
            "service": "database",
            "status": "PENDING",
            "environment": "staging"
        }
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
