import pytest
from jose import jwt

from app.config import settings


@pytest.mark.parametrize("password", ["x" * 73, "é" * 37])
def test_password_byte_limit(client, password):
    response = client.post("/auth/register", json={
        "email": "long@example.com", "name": "Long Password", "password": password,
    })
    assert response.status_code == 422


def test_password_at_bcrypt_limit(client):
    password = "x" * 72
    assert client.post("/auth/register", json={
        "email": "limit@example.com", "name": "Limit User", "password": password,
    }).status_code == 201
    assert client.post("/auth/login", data={
        "username": "limit@example.com", "password": password,
    }).status_code == 200
    assert client.post("/auth/login", data={
        "username": "limit@example.com", "password": password + "x",
    }).status_code == 401


def test_null_project_name(client, auth_headers, project):
    response = client.patch(f"/projects/{project['id']}",
                            json={"name": None}, headers=auth_headers)
    assert response.status_code == 422


@pytest.mark.parametrize("field", ["title", "priority", "status"])
def test_null_task_fields(client, auth_headers, project, field):
    task = client.post(f"/projects/{project['id']}/tasks", headers=auth_headers,
                       json={"title": "Regression task", "priority": 2}).json()
    response = client.patch(f"/tasks/{task['id']}", headers=auth_headers,
                            json={field: None})
    assert response.status_code == 422


def test_assignment_validation_and_clear(client, auth_headers, project):
    task = client.post(f"/projects/{project['id']}/tasks", headers=auth_headers,
                       json={"title": "Assigned task", "priority": 2,
                             "due_date": "2026-10-07"}).json()
    url = f"/tasks/{task['id']}"
    assert client.post(url + "/assign", headers=auth_headers,
                       json={"user_id": 9999}).status_code == 404
    assert client.patch(url, headers=auth_headers,
                        json={"assignee_id": 9999}).status_code == 404
    response = client.post(url + "/assign", headers=auth_headers,
                           json={"user_id": project['owner_id']})
    assert response.status_code == 200
    response = client.patch(url, headers=auth_headers,
                            json={"assignee_id": None, "due_date": None})
    assert response.status_code == 200
    assert response.json()["assignee_id"] is None
    assert response.json()["due_date"] is None


@pytest.mark.parametrize("subject", [None, [], {}, "invalid"])
def test_invalid_token_subject(client, subject):
    token = jwt.encode({"sub": subject}, settings.secret_key, algorithm="HS256")
    assert client.get("/projects", headers={
        "Authorization": f"Bearer {token}",
    }).status_code == 401
