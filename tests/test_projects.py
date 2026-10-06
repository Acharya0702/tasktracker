from fastapi.testclient import TestClient


def test_create_project(
    client: TestClient, auth_headers: dict
):
    response = client.post(
        "/projects",
        json={"name": "My Project"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "My Project"


def test_list_projects(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_project(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.get(
        f"/projects/{project['id']}", headers=auth_headers
    )
    assert response.status_code == 200


def test_get_missing_project(
    client: TestClient, auth_headers: dict
):
    response = client.get("/projects/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_project(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.patch(
        f"/projects/{project['id']}",
        json={"name": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_delete_project(
    client: TestClient, auth_headers: dict, project: dict
):
    response = client.delete(
        f"/projects/{project['id']}", headers=auth_headers
    )
    assert response.status_code == 204


def test_invalid_project_name(
    client: TestClient, auth_headers: dict
):
    response = client.post(
        "/projects",
        json={"name": "ab"},
        headers=auth_headers,
    )
    assert response.status_code == 422