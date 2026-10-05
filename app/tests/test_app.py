import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_tasks_start_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json == {"tasks": []}


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Write demo story"})

    assert response.status_code == 201
    assert response.json == {"id": 1, "title": "Write demo story", "completed": False}


def test_create_task_requires_title(client):
    response = client.post("/tasks", json={"title": "  "})

    assert response.status_code == 400
    assert response.json == {"error": "title is required"}


def test_update_task(client):
    client.post("/tasks", json={"title": "Task 1"})
    response = client.patch("/tasks/1", json={"completed": True})

    assert response.status_code == 200
    assert response.json == {"id": 1, "title": "Task 1", "completed": True}


def test_update_task_not_found(client):
    response = client.patch("/tasks/999", json={"completed": True})

    assert response.status_code == 404