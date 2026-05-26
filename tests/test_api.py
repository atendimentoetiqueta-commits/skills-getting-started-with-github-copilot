import pytest
from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
    }


def test_get_activities_returns_activity_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"Chess Club", "Programming Class"}
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    assert data["Programming Class"]["participants"] == [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]


def test_signup_adds_participant_to_activity():
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Signed up newstudent@mergington.edu for Chess Club"
    )
    assert "newstudent@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity():
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant():
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity():
    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete(
        "/activities/Chess%20Club/participants?email=missing%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_returns_404_for_unknown_activity():
    response = client.delete(
        "/activities/Unknown%20Club/participants?email=missing%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
