from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_cache_hit():
    client.post("/v1/run", json={"value": "Hello   World"})
    response = client.post("/v1/run", json={"value": "hello world"})
    assert response.json()["cache_hit"] is True
