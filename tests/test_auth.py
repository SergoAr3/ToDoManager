import json

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from ToDoManager.app.db import User


@pytest.mark.parametrize(
    'user_data',
    [
        {
            "username": "Sergo",
            "password": "Ser060702!",
        }
    ]
)
async def test_create_user(client: TestClient, async_session_test, user_data):
    resp = client.post("/auth/register", content=json.dumps(user_data))
    assert resp.status_code == 204
    async with async_session_test() as session:
        user_from_db = await session.execute(select(User).where(User.username == user_data["username"]))
    user_from_db = user_from_db.scalar()
    assert user_from_db.username == user_data["username"]
    assert user_from_db.is_active is True


@pytest.mark.parametrize(
    'user_data, user_data_same',
    [
        (
                {
                    "username": "Sergo",
                    "hashed_password": bytes(333),
                },
                {
                    "username": "Sergo",
                    "password": "12981246",
                }
        )
    ]

)
async def test_create_user_already_exists(client: TestClient, async_session_test, user_data, user_data_same):
    user = User(**user_data)
    async with async_session_test() as session:
        session.add(user)
        await session.commit()
    resp = client.post("/auth/register", content=json.dumps(user_data_same))
    assert resp.status_code == 409
    assert (
            'User with this username already exists!'
            in resp.json()["detail"]
    )
