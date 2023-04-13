"""Unit tests for api"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_measurements() -> None:
    """Test response code"""
    response = client.post("/measurement/")
    print(response.status_code)
    assert response.status_code == 422
