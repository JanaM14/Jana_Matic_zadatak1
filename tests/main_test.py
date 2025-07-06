from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_get_tickets():
    response = client.get("/tickets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_ticket_by_id_found():
    response = client.get("/tickets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_ticket_by_id_not_found():
    response = client.get("/tickets/999999")
    assert response.status_code == 404


def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "status_counts" in data and "priority_counts" in data
