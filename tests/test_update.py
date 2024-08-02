import json
from datetime import datetime

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from ToDoManager.app.db import Task, User, TaskAccess
from ToDoManager.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'task_data, update_task_data, user_data, user2_data, access_data',
    [
        (
                {
                    "id": 1,
                    "title": "Задача",
                    "description": "Моя задача",
                    'owner_id': 1
                },
                {
                    "description": "Описание задачи",
                    "status": "in progress"
                },
                {
                    'id': 1,
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                },
                {
                    'id': 2,
                    "username": "Anton A.",
                    "hashed_password": bytes(233333),
                },
                {
                    'task_id': 1,
                    "user_id": 2,
                    "access_id": 1,
                },

        )

    ]
)
async def test_update_task(client: TestClient, async_session_test, task_data, update_task_data, user_data, user2_data,
                           access_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    headers2 = await create_test_auth_headers_for_user(user2_data['username'])
    task = Task(**task_data)
    user = User(**user_data)
    user2 = User(**user2_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(user2)
        await session.flush()
        session.add(task)
        await session.commit()

    resp = client.patch(f"/task/{task.id}", content=json.dumps(update_task_data), headers=headers)
    time_now = datetime.strftime(datetime.now(), "%H:%M:%S %d-%m-%Y")
    assert resp.status_code == 204

    async with async_session_test() as session:
        created_task = await session.execute(select(Task).where(Task.id == task_data['id']))
        created_task = created_task.scalar()

    updated_at = datetime.strftime(created_task.updated_at, "%H:%M:%S %d-%m-%Y")

    assert created_task.description == update_task_data['description']
    assert updated_at == time_now
    assert created_task.status == update_task_data['status']

    resp = client.patch(f"/task/{task.id}", content=json.dumps(update_task_data), headers=headers2)
    assert resp.status_code == 403

    access = TaskAccess(**access_data)
    async with async_session_test() as session:
        session.add(access)
        await session.commit()

    resp = client.patch(f"/task/{task.id}", content=json.dumps(update_task_data), headers=headers)
    time_now = datetime.strftime(datetime.now(), "%H:%M:%S %d-%m-%Y")
    assert resp.status_code == 204

    async with async_session_test() as session:
        created_task = await session.execute(select(Task).where(Task.id == task_data['id']))
        created_task = created_task.scalar()

    updated_at = datetime.strftime(created_task.updated_at, "%H:%M:%S %d-%m-%Y")

    assert created_task.description == update_task_data['description']
    assert updated_at == time_now
    assert created_task.status == update_task_data['status']
