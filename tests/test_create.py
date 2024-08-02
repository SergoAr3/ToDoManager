import json
from datetime import datetime

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
                    "title": "Задача",
                    "description": "Моя задача",
                },
                {
                    'id': 1,
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                }

        )

    ]
)
async def test_create_task(client: TestClient, async_session_test, task_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    async with async_session_test() as session:
        session.add(user)
        await session.commit()
    resp = client.post(f"/task", content=json.dumps(task_data), headers=headers)
    time_now = datetime.strftime(datetime.now(), "%H:%M:%S %d-%m-%Y")
    assert resp.status_code == 204

    async with async_session_test() as session:
        created_task = await session.execute(select(Task).where(Task.title == task_data['title']))
        created_task = created_task.scalar()

    created_at = datetime.strftime(created_task.created_at, "%H:%M:%S %d-%m-%Y")
    updated_at = datetime.strftime(created_task.updated_at, "%H:%M:%S %d-%m-%Y")

    assert created_task.description == task_data['description']
    assert created_at == time_now
    assert updated_at == time_now
    assert created_task.status == 'not started'
    assert created_task.owner_id == user_data['id']
