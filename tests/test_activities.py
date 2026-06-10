import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_successful_signup(client):
    # Arrange
    activity = "Soccer Team"
    email = "tester@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body["message"]
    # Verify participant appears in GET
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already present in initial data

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"].lower()


def test_signup_missing_activity_returns_404(client):
    # Arrange
    activity = "No Such Activity"
    email = "someone@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "activity not found" in resp.json()["detail"].lower()


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Sanity check participant exists
    before = client.get("/activities").json()
    assert email in before[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "removed" in resp.json()["message"].lower()
    after = client.get("/activities").json()
    assert email not in after[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "participant not found" in resp.json()["detail"].lower()
