from src.app import activities


def test_unregister_success(client):
    # Arrange: ensure the user is signed up
    activity = "Music Band"
    email = "unreg_user@example.com"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Act: unregister the user
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert: successful unregister and message contains email
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed_up(client):
    # Arrange: ensure the user is NOT signed up
    activity = "Gym Class"
    email = "not_signed@example.com"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act: attempt to unregister
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert: receives 400 with appropriate detail
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student is not signed up for this activity"
