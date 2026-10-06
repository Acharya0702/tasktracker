from fastapi.testclient import TestClient


def test_create_task(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "Write tests", "priority": 2},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["status"] == "todo"


def test_short_title(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "ab", "priority": 2},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_invalid_priority(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "Valid title", "priority": 100},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_list_tasks(
    client: TestClient, auth_headers: dict, project: dict
):
    client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "Task 1", "priority": 2},
        headers=auth_headers,
    )
    response = client.get(
        f"/projects/{project['id']}/tasks", headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_tasks_by_status(
    client: TestClient, auth_headers: dict, project: dict
):
    client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "Task 1", "priority": 2},
        headers=auth_headers,
    )
    response = client.get(
        f"/projects/{project['id']}/tasks?status=done",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_update_task(
    client: TestClient, auth_headers: dict, project: dict
):
    created = client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "Task to update", "priority": 2},
        headers=auth_headers,
    ).json()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"status": "doing"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "doing"


def test_delete_task(
    client: TestClient, auth_headers: dict, project: dict
):
    created = client.post(
        f"/projects/{project['id']}/tasks",
        json={"title": "Task to delete", "priority": 2},
        headers=auth_headers,
    ).json()

    response = client.delete(
        f"/tasks/{created['id']}", headers=auth_headers
    )
    assert response.status_code == 204


def test_get_missing_task(
    client: TestClient, auth_headers: dict
):
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_user_cannot_access_other_users_data(
    client: TestClient, auth_headers: dict, project: dict
):
    # Second user
    client.post(
        "/auth/register",
        json={
            "email": "other@example.com",
            "name": "Other",
            "password": "password123",
        },
    )
    other_token = client.post(
        "/auth/login",
        data={"username": "other@example.com", "password": "password123"},
    ).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # Try to access first user's project
    response = client.get(
        f"/projects/{project['id']}", headers=other_headers
    )
    assert response.status_code == 404