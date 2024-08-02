import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from ToDoManager.app.db import Task, User
from ToDoManager.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'task_data, user_data',
    [
        (
                {
                    "id": 1,
                    "title": "Задача",
                    "description": "Моя задача",
                    'owner_id': 1
                },
                {
                    'id': 1,
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                }

        )

    ]
)
async def test_delete_task(client: TestClient, async_session_test, task_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    task = Task(**task_data)
    async with async_session_test() as session:
        session.add(user)
        await session.flush()
        session.add(task)
        await session.commit()

    resp = client.delete(f"/task/{task.id}", headers=headers)
    assert resp.status_code == 204

    async with async_session_test() as session:
        task_id = await session.execute(select(Task.id).where(Task.id == task_data['id']))
        task_id = task_id.scalar()
    assert task_id is None
