from app.db.models import User
from app.utils.password import hash_password
from app.utils.session_store import sessions
from app.utils.jwt_handler import create_access_token


def create_auth_user(db_session, *, user_id=1, name="Auth User", email="auth@example.com", password="strongpassword123", role="user"):
    user = User(
        id=user_id,
        name=name,
        email=email,
        password=hash_password(password),
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_login_jwt_success(client, db_session):
    create_auth_user(db_session)

    payload = {
        "email": "auth@example.com",
        "password": "strongpassword123",
    }

    response = client.post("/auth/login-jwt", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_jwt_invalid_email(client):
    payload = {
        "email": "missing@example.com",
        "password": "strongpassword123",
    }

    response = client.post("/auth/login-jwt", json=payload)

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["type"] == "http_error"
    assert data["error"]["message"] == "Invalid credentials"


def test_login_jwt_invalid_password(client, db_session):
    create_auth_user(db_session)

    payload = {
        "email": "auth@example.com",
        "password": "wrongpassword",
    }

    response = client.post("/auth/login-jwt", json=payload)

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Invalid credentials"


def test_login_jwt_validation_error(client):
    payload = {
        "email": "auth@example.com",
    }

    response = client.post("/auth/login-jwt", json=payload)

    assert response.status_code == 422
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["type"] == "validation_error"


def test_me_jwt_success(client):
    token = create_access_token({
        "sub": "auth@example.com",
        "role": "user",
        "user_id": 1,
    })

    response = client.get(
        "/auth/me-jwt",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Authenticated with JWT"
    assert data["user"]["sub"] == "auth@example.com"
    assert data["user"]["role"] == "user"
    assert data["user"]["user_id"] == 1


def test_me_jwt_invalid_token(client):
    response = client.get(
        "/auth/me-jwt",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Invalid or expired token"


def test_me_jwt_missing_token(client):
    response = client.get("/auth/me-jwt")

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["type"] == "http_error"
    assert data["error"]["message"] == "Not authenticated"


def test_login_session_success(client, db_session):
    sessions.clear()
    create_auth_user(db_session)

    payload = {
        "email": "auth@example.com",
        "password": "strongpassword123",
    }

    response = client.post("/auth/login-session", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Logged in with session"
    assert "session_id=" in response.headers.get("set-cookie", "")


def test_login_session_invalid_credentials(client):
    sessions.clear()

    payload = {
        "email": "missing@example.com",
        "password": "strongpassword123",
    }

    response = client.post("/auth/login-session", json=payload)

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Invalid credentials"


def test_me_session_success(client, db_session):
    sessions.clear()
    create_auth_user(db_session)

    login_payload = {
        "email": "auth@example.com",
        "password": "strongpassword123",
    }

    login_response = client.post("/auth/login-session", json=login_payload)
    assert login_response.status_code == 200

    response = client.get("/auth/me-session")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Authenticated with session"
    assert data["user"]["email"] == "auth@example.com"
    assert data["user"]["role"] == "user"


def test_me_session_no_cookie(client):
    sessions.clear()
    client.cookies.clear()

    response = client.get("/auth/me-session")

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "No session cookie found"


def test_me_session_invalid_session(client):
    sessions.clear()
    client.cookies.set("session_id", "fake-session-id")

    response = client.get("/auth/me-session")

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Invalid session"


def test_logout_session_success(client, db_session):
    sessions.clear()
    create_auth_user(db_session)

    login_payload = {
        "email": "auth@example.com",
        "password": "strongpassword123",
    }

    login_response = client.post("/auth/login-session", json=login_payload)
    assert login_response.status_code == 200
    assert len(sessions) == 1

    response = client.post("/auth/logout-session")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Logged out from session"
    assert len(sessions) == 0


def test_logout_session_without_cookie_still_succeeds(client):
    sessions.clear()
    client.cookies.clear()

    response = client.post("/auth/logout-session")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Logged out from session"


def test_protected_jwt_success(client):
    token = create_access_token({
        "sub": "auth@example.com",
        "role": "user",
        "user_id": 1,
    })

    response = client.get(
        "/auth/protected-jwt",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "You are authenticated"
    assert data["user"]["sub"] == "auth@example.com"


def test_protected_jwt_invalid_token(client):
    response = client.get(
        "/auth/protected-jwt",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Invalid or expired token"


def test_admin_jwt_success(client):
    token = create_access_token({
        "sub": "admin@example.com",
        "role": "admin",
        "user_id": 99,
    })

    response = client.get(
        "/auth/admin-jwt",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Welcome Admin"
    assert data["user"]["role"] == "admin"


def test_admin_jwt_forbidden_for_non_admin(client):
    token = create_access_token({
        "sub": "auth@example.com",
        "role": "user",
        "user_id": 1,
    })

    response = client.get(
        "/auth/admin-jwt",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Forbidden"


def test_admin_jwt_invalid_token(client):
    response = client.get(
        "/auth/admin-jwt",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Invalid or expired token"