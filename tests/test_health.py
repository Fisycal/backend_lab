from app.main import app
from app.db.database import get_db


def test_health_live(client):
    response = client.get("/health/live")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "alive"
    assert "service" in data
    assert "environment" in data
    assert "version" in data


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "version" in data
    assert "environment" in data


def test_health_ready_success(client):
    response = client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ready"
    assert data["database"] == "ok"


def test_health_success(client):
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["database"] == "ok"


def test_health_failure_returns_503(client):
    class BrokenSession:
        def execute(self, *args, **kwargs):
            raise Exception("DB unavailable")

    def override_broken_db():
        yield BrokenSession()

    original_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_broken_db

    try:
        response = client.get("/health")

        assert response.status_code == 503
        data = response.json()

        assert data["status"] == "error"
        assert data["error"]["type"] == "http_error"

        detail = data["error"]["message"]
        assert detail["status"] == "degraded"
        assert detail["database"] == "error"
    finally:
        if original_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = original_override
