import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


def override_get_db():
    database = TestSessionLocal()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_create_list_update_and_delete_task(client):
    created = client.post(
        "/tasks",
        json={
            "title": "Finish lab",
            "description": "Submit the Python assignment",
            "student_name": "Alex",
        },
    )
    assert created.status_code == 201
    task = created.json()
    assert task["completed"] is False

    listed = client.get("/tasks")
    assert listed.status_code == 200
    assert listed.json() == [task]

    updated = client.patch(f"/tasks/{task['id']}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/tasks/{task['id']}")
    assert deleted.status_code == 204
    assert client.get("/tasks").json() == []


def test_update_missing_task_returns_404(client):
    response = client.patch("/tasks/999", json={"completed": True})
    assert response.status_code == 404
