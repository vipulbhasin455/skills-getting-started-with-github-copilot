from src.app import activities


def test_root_redirect(client):
    # Arrange: prepare no special state
    # Act: request root without following redirects
    resp = client.get("/", allow_redirects=False)

    # Assert: response is a redirect to the static index
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location", "").endswith("/static/index.html")


def test_get_activities(client):
    # Arrange: ensure activities exist
    assert isinstance(activities, dict)

    # Act: fetch activities
    resp = client.get("/activities")

    # Assert: successful response and payload contains known key
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
