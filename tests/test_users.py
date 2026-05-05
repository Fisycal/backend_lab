from app.utils.password import hash_password

def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_get_users_empty(client):
    response = client.get("/users/")

    assert response.status_code == 200
    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["pages"] == 0


def test_create_user_success(client):
    payload = {
        "id": 1,
        "name": "Michael",
        "email": "michael@example.com",
        "password": "strongpassword123",
        "role": "user",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Michael"
    assert data["email"] == "michael@example.com"
    assert data["role"] == "user"
    assert "password" not in data


def test_get_users_returns_created_user(client):
    payload = {
        "id": 1,
        "name": "Michael",
        "email": "michael@example.com",
        "password": "strongpassword123",
        "role": "user",
    }
    client.post("/users/", json=payload)

    response = client.get("/users/")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == 1
    assert data["items"][0]["email"] == "michael@example.com"


def test_get_user_by_id_success(client, sample_user, admin_token):
    response = client.get(
        "/users/1",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Michael"
    assert data["email"] == "michael@example.com"


def test_get_user_not_found(client, admin_token):
    response = client.get(
        "/users/999",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 404
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["type"] == "http_error"
    assert data["error"]["message"] == "User not found"


def test_create_user_duplicate_id(client, sample_user):
    payload = {
        "id": 1,
        "name": "Another User",
        "email": "another@example.com",
        "password": "strongpassword123",
        "role": "user",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 400
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "User ID already exists"


def test_create_user_duplicate_email(client, sample_user):
    payload = {
        "id": 2,
        "name": "Another User",
        "email": "michael@example.com",
        "password": "strongpassword123",
        "role": "user",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 400
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Email already exists"


def test_create_user_validation_error(client):
    payload = {
        "id": 1,
        "name": "Michael",
        "email": "michael@example.com",
        "role": "user",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 422
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["type"] == "validation_error"


def test_replace_user_success(client, sample_user, admin_token):
    payload = {
        "id": 1,
        "name": "Michael Randy",
        "email": "michael.randy@example.com",
        "password": "newstrongpassword123",
        "role": "user",
    }

    response = client.put(
        "/users/1",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Michael Randy"
    assert data["email"] == "michael.randy@example.com"


def test_replace_user_path_body_id_mismatch(client, sample_user, admin_token):
    payload = {
        "id": 2,
        "name": "Mismatch User",
        "email": "mismatch@example.com",
        "password": "newstrongpassword123",
        "role": "user",
    }

    response = client.put(
        "/users/1",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 400
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["type"] == "http_error"
    assert data["error"]["message"] == "Path user_id must match body id"


def test_replace_user_not_found(client, admin_token):
    payload = {
        "id": 999,
        "name": "Ghost User",
        "email": "ghost.user@example.com",
        "password": "newstrongpassword123",
        "role": "user",
    }

    response = client.put(
        "/users/999",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 404
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "User not found"


def test_replace_user_duplicate_email(client, sample_user, db_session, admin_token):
    from app.db.models import User

    another_user = User(
        id=2,
        name="Second User",
        email="second.user@example.com",
        password=hash_password("strongpassword123"),
        role="user",
    )
    db_session.add(another_user)
    db_session.commit()

    payload = {
        "id": 1,
        "name": "Michael Randy",
        "email": "second.user@example.com",
        "password": "newstrongpassword123",
        "role": "user",
    }

    response = client.put(
        "/users/1",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 400
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Email already exists"


def test_patch_user_success(client, sample_user, admin_token):
    payload = {
        "name": "Patched Michael"
    }

    response = client.patch(
        "/users/1",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Patched Michael"
    assert data["email"] == "michael@example.com"


def test_patch_user_email_success(client, sample_user, admin_token):
    payload = {
        "email": "patched@example.com"
    }

    response = client.patch(
        "/users/1",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "patched@example.com"


def test_patch_user_not_found(client, admin_token):
    payload = {
        "name": "Nobody"
    }

    response = client.patch(
        "/users/999",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 404
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "User not found"


def test_patch_user_duplicate_email(client, sample_user, db_session, admin_token):
    from app.db.models import User

    another_user = User(
        id=2,
        name="Second User",
        email="second.user@example.com",
        password=hash_password("strongpassword123"),
        role="user",
    )
    db_session.add(another_user)
    db_session.commit()

    payload = {
        "email": "second.user@example.com"
    }

    response = client.patch(
        "/users/1",
        json=payload,
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 400
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Email already exists"


def test_delete_user_success(client, sample_user, admin_token):
    response = client.delete(
        "/users/1",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 204
    assert response.text == ""

    get_response = client.get(
        "/users/1",
        headers=auth_headers(admin_token),
    )
    assert get_response.status_code == 404


def test_delete_user_not_found(client, admin_token):
    response = client.delete(
        "/users/999",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 404
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "User not found"


def test_head_users(client):
    response = client.head("/users/")

    assert response.status_code == 200


def test_head_user_success(client, sample_user):
    response = client.head("/users/1")

    assert response.status_code == 200


def test_head_user_not_found(client):
    response = client.head("/users/999")

    assert response.status_code == 404
    assert response.text == ""


def test_options_users(client):
    response = client.options("/users/")

    assert response.status_code == 200
    assert "Allow" in response.headers
    assert response.headers["Allow"] == "GET, POST, HEAD, OPTIONS"


def test_options_user_success(client, sample_user):
    response = client.options("/users/1")

    assert response.status_code == 200
    assert "Allow" in response.headers
    assert response.headers["Allow"] == "GET, PUT, PATCH, DELETE, HEAD, OPTIONS"


def test_options_user_not_found(client):
    response = client.options("/users/999")

    assert response.status_code == 404
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "User not found"


def test_user_can_access_own_profile(client, sample_user, normal_user_token):
    response = client.get(
        "/users/1",
        headers=auth_headers(normal_user_token),
    )

    assert response.status_code == 200


def test_user_cannot_access_other_user_profile(
    client,
    sample_user,
    db_session,
    normal_user_token,
    ):
    from app.db.models import User
    from app.utils.password import hash_password

    another_user = User(
        id=2,
        name="Second User",
        email="second.user@example.com",
        password=hash_password("strongpassword123"),
        role="user",
    )
    db_session.add(another_user)
    db_session.commit()

    response = client.get(
        "/users/2",
        headers=auth_headers(normal_user_token),
    )

    assert response.status_code == 403
    data = response.json()

    assert data["status"] == "error"
    assert data["error"]["message"] == "Forbidden"
    

def test_admin_can_access_any_user(
    client,
    sample_user,
    db_session,
    admin_token,
):
    from app.db.models import User

    another_user = User(
        id=2,
        name="Second User",
        email="second.user@example.com",
        password=hash_password("strongpassword123"),
        role="user",
    )
    db_session.add(another_user)
    db_session.commit()

    response = client.get(
        "/users/2",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200


def test_get_users_pagination(client):
    for i in range(1, 4):
        payload = {
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "password": "strongpassword123",
            "role": "user",
        }
        client.post("/users/", json=payload)

    response = client.get("/users/?page=1&size=2")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 3
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["pages"] == 2
    assert len(data["items"]) == 2


def test_get_users_filter_by_role(client):
    client.post("/users/", json={
        "id": 1,
        "name": "Regular User",
        "email": "user@example.com",
        "password": "strongpassword123",
        "role": "user",
    })

    client.post("/users/", json={
        "id": 2,
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "strongpassword123",
        "role": "admin",
    })

    response = client.get("/users/?role=admin")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["role"] == "admin"

def test_get_users_search_by_name(client):
    client.post("/users/", json={
        "id": 1,
        "name": "Michael",
        "email": "michael@example.com",
        "password": "strongpassword123",
        "role": "user",
    })

    client.post("/users/", json={
        "id": 2,
        "name": "Toyin",
        "email": "toyin@example.com",
        "password": "strongpassword123",
        "role": "user",
    })

    response = client.get("/users/?search=Michael")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["name"] == "Michael"