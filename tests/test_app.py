import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def test_home_page():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Deployment Control Center" in response.data


def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_status_endpoint():
    response = app.test_client().get("/api/status")
    assert response.status_code == 200
    assert response.json["application"] == "online"


def test_deployments_endpoint():
    response = app.test_client().get("/api/deployments")
    assert response.status_code == 200
    assert len(response.json) == 3
