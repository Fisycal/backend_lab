import os
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["APP_NAME"] = "Backend Concepts Lab"
os.environ["APP_VERSION"] = "0.1.0"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User

from app.utils.password import hash_password


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user(db_session):
    user = User(
        id=1,
        name="Michael",
        email="michael@example.com",
        password=hash_password("strongpassword123"),
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

import pytest


@pytest.fixture
def admin_user(client):
    payload = {
        "id": 100,
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpassword123",
        "role": "admin",
    }

    response = client.post("/users/", json=payload)
    assert response.status_code in (201, 400)

    return payload


@pytest.fixture
def normal_user(client):
    payload = {
        "id": 1,
        "name": "Michael",
        "email": "michael@example.com",
        "password": "strongpassword123",
        "role": "user",
    }

    response = client.post("/users/", json=payload)
    assert response.status_code in (201, 400)

    return payload


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        "/auth/login-jwt",
        json={
            "email": "admin@example.com",
            "password": "adminpassword123",
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def normal_user_token(client, normal_user):
    response = client.post(
        "/auth/login-jwt",
        json={
            "email": "michael@example.com",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]