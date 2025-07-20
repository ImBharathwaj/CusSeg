from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ingest_valid():
    response = client.post("/ingest", json = {
        "customer_id": "123",
        "attributes": {"email":"123@gomail.com"}
    })
    assert response.status_code == 200
    assert "Ingestion successful" in response.json()["message"]

def test_ingest_invalid():
    response = client.post("ingest", json={})
    assert response.status_code == 422  # Unprocessable Entity
