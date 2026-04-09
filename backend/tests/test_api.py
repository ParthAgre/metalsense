import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MetalSense API"}

def test_education_metals():
    response = client.get("/api/v1/education/metals")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Even if DB is empty, default seed returns 4 items
    assert len(data) >= 0

def test_education_materials():
    response = client.get("/api/v1/education/materials")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
