import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_piece():
    response = client.post("/pieces", json={"name": "Torse", "color": "Jaune", "quantity": 13})
    assert response.status_code == 201
    piece = response.json()
    assert piece["name"] == "Torse"
    assert piece["model_id"] is None

    response = client.get("/pieces/available")
    assert response.status_code == 200
    available = response.json()
    assert any(p["id"] == piece["id"] for p in available)