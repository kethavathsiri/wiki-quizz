from fastapi.testclient import TestClient
from main import app


def test_health_endpoint():
    client = TestClient(app)
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert data["status"] in ("healthy", "degraded") or isinstance(data["llm_initialized"], bool)
