import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from ToDoManager.app.db import Task, User, TaskAccess
from ToDoManager.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'task_data, user_data, user2_data, query_params',
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
                    "user_id": 2,
                    "access": "editor"
                },

        )

    ]
)
async def test_assign_access(client: TestClient, async_session_test, task_data, user_data, user2_data, query_params):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    task = Task(**task_data)
    user = User(**user_data)
    user2 = User(**user2_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(user2)
        await session.flush()
        session.add(task)
        await session.commit()
    resp = client.post(f"/task/{task.id}/access", headers=headers, params=query_params)
    assert resp.status_code == 204

    async with async_session_test() as session:
        created_access = await session.execute(select(TaskAccess).where(TaskAccess.task_id == task.id))
        created_access = created_access.scalar()

    assert created_access.user_id == 2
    assert created_access.access_id == 2


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
                    "access_id": 1
                },

        )

    ]
)
async def test_revoke_access(client: TestClient, async_session_test, task_data, user_data, user2_data, access_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    task = Task(**task_data)
    user = User(**user_data)
    user2 = User(**user2_data)
    access = TaskAccess(**access_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(user2)
        await session.flush()
        session.add(task)
        await session.flush()
        session.add(access)
        await session.commit()
    resp = client.delete(f"/task/{task.id}/access", headers=headers, params={"user_id": user2.id})

    assert resp.status_code == 204

    async with async_session_test() as session:
        created_access = await session.execute(select(TaskAccess).where(TaskAccess.task_id == task.id))
        created_access = created_access.scalar()

    assert created_access is None
