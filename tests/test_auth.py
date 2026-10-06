from fastapi.testclient import TestClient


def test_register(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "name": "New User",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "password" not in data


def test_register_duplicate_email(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "name": "User",
            "password": "password123",
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "name": "User2",
            "password": "password123",
        },
    )
    assert response.status_code == 409


def test_login_success(client: TestClient, auth_headers: dict):
    assert "Authorization" in auth_headers


def test_login_wrong_password(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "wrong@example.com",
            "name": "User",
            "password": "correct123",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "wrong@example.com", "password": "wrong123"},
    )
    assert response.status_code == 401


def test_protected_route_without_token(client: TestClient):
    response = client.get("/projects")
    assert response.status_code == 401