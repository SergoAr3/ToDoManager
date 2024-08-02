import json
from datetime import datetime

import pytest
from starlette.testclient import TestClient

from ToDoManager.app.db import Task, User, TaskAccess
from ToDoManager.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'task_data, user_data, user2_data, access_data',
    [
        (

                {
                    "id": 1,
                    "title": "Задача",
                    "description": "Моя задача",
                    "owner_id": 1
                },
                {
                    "id": 1,
                    "username": "Sergey H.",
                    "hashed_password": bytes(121241),
                },
                {
                    "id": 2,
                    "username": "Anton A.",
                    "hashed_password": bytes(233333),
                },
                {
                    "task_id": 1,
                    "user_id": 2,
                    "access_id": 1,
                },

        )

    ]
)
async def test_get_task(client: TestClient, async_session_test, task_data, user_data, user2_data, access_data):
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
        time_now = datetime.strftime(datetime.now(), "%H:%M:%S %d-%m-%Y")
    resp = client.get(f"/task/{task.id}", headers=headers)
    resp_content = json.loads(resp.content.decode("utf-8"))

    assert resp.status_code == 200
    assert resp_content['id'] == task_data['id']
    assert resp_content['title'] == task_data['title']
    assert resp_content['description'] == task_data['description']
    assert resp_content['created_at'] == time_now
    assert resp_content['updated_at'] == time_now
    assert resp_content['owner'] == user.username

    resp = client.get(f"/task/{task.id}", headers=headers2)
    assert resp.status_code == 403

    access = TaskAccess(**access_data)
    async with async_session_test() as session:
        session.add(access)
        await session.commit()

    resp = client.get(f"/task/{task.id}", headers=headers2)
    assert resp.status_code == 200
    assert resp_content['id'] == task_data['id']
    assert resp_content['title'] == task_data['title']
    assert resp_content['description'] == task_data['description']
    assert resp_content['created_at'] == time_now
    assert resp_content['updated_at'] == time_now
    assert resp_content['owner'] == user.username
