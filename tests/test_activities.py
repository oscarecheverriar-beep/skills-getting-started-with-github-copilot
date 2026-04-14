import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    
    # Verify participant was added
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")  # First signup
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid Activity"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_remove_participant_success():
    # Arrange
    email = "remove@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")  # Add participant first
    
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    
    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity]["participants"]

def test_remove_participant_not_found():
    # Arrange
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]

def test_remove_participant_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid Activity"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]