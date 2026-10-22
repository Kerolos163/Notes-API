
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_notes():
    response = client.get("/notes")
    
    assert response.status_code == 200
    assert response.json() == {"notes": [
        {"id": 1, "title": "Note 1"},
        {"id": 2, "title": "Note 2"},   
        {"id": 3, "title": "Note 3"}
    ]}
