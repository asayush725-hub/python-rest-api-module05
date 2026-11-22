import os
from fastapi.testclient import TestClient

import database
from main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "dev-secret-key-123"}
TEST_DB = "test_tasks.db"


def setup_function():
    # Point database module to a temporary test DB so real tasks.db stays clean
    database.DB_NAME = TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    database.init_db()


def teardown_function():
    try:
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    except PermissionError:
        pass


def test_health_check():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "message": "API is running"}


def test_missing_and_invalid_api_key():
    # Missing X-API-Key header
    no_key = client.get("/tasks")
    assert no_key.status_code in (401, 422)

    # Wrong X-API-Key value
    bad_key = client.get("/tasks", headers={"X-API-Key": "wrong-key"})
    assert bad_key.status_code == 401


def test_validation_error_on_empty_title():
    res = client.post("/tasks", json={"title": ""}, headers=HEADERS)
    assert res.status_code == 422


def test_full_crud_lifecycle():
    # 1. Create (POST -> 201)
    created = client.post(
        "/tasks",
        json={"title": "Test Module 05 API", "description": "Verify CRUD flow"},
        headers=HEADERS,
    )
    assert created.status_code == 201
    created_data = created.json()
    task_id = created_data["id"]
    assert created_data["title"] == "Test Module 05 API"
    assert created_data["completed"] is False

    # 2. Read single & list (GET -> 200)
    fetched = client.get(f"/tasks/{task_id}", headers=HEADERS)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == task_id

    listed = client.get("/tasks", headers=HEADERS)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    # 3. Update (PUT -> 200)
    updated = client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=HEADERS,
    )
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    # 4. Delete (DELETE -> 204)
    deleted = client.delete(f"/tasks/{task_id}", headers=HEADERS)
    assert deleted.status_code == 204

    # 5. Confirm 404 after deletion
    after_delete = client.get(f"/tasks/{task_id}", headers=HEADERS)
    assert after_delete.status_code == 404