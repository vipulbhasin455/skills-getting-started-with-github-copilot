from src.app import activities


def test_signup_success(client):
    # Arrange: pick an activity and ensure test email is not present
    activity = "Debate Team"
    email = "test_user@example.com"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act: sign up the user
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: successful signup and message contains email and activity
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")
    assert email in activities[activity]["participants"]

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)


def test_signup_duplicate(client):
    # Arrange: ensure the user is signed up once
    activity = "Programming Class"
    email = "duplicate_user@example.com"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Act: attempt to sign up again
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: API returns 400 for duplicate signup
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student is already signed up for this activity"

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
