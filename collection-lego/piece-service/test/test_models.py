import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_model():
    response = client.post("/models", json={"name": "L-établi Minecfaft"})
    assert response.status_code == 201
    model = response.json()
    assert model["name"] == "L-établi Minecfaft"
    assert model["pieces"] == []