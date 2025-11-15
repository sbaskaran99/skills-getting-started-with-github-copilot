import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Ensure not already registered
    client.delete(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]

    # Unregister
    response_unreg = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response_unreg.status_code == 200
    assert (
        f"Unregistered {test_email}" in response_unreg.json()["message"]
        or f"was not registered" in response_unreg.json()["message"]
    )

    # Unregister again (should be idempotent)
    response_unreg2 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response_unreg2.status_code == 200
    assert f"was not registered" in response_unreg2.json()["message"]
