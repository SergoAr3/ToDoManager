import asyncio
import os
from typing import Any, Generator, Mapping

import pytest
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
from starlette.testclient import TestClient

from ToDoManager.app.auth.utils import encode_jwt
from ToDoManager.app.db.db import get_db

from ToDoManager.main import app

load_dotenv('../.env-test')

CLEAN_TABLES = [
    'task',
    'user',
    'task_access',
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test() -> async_sessionmaker:
    engine = create_async_engine(os.getenv('TEST_DATABASE_URL'), future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"""TRUNCATE TABLE "{table_for_cleaning}" CASCADE;"""))


async def _get_test_db():
    try:
        test_engine = create_async_engine(
            os.getenv('TEST_DATABASE_URL'), future=True,
        )

        test_async_session = async_sessionmaker(
            test_engine, expire_on_commit=False
        )
        async with test_async_session() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                logger.error(e)
                await session.rollback()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


async def create_test_auth_headers_for_user(username: str) -> Mapping[str, str]:
    jwt_payload = {
        'sub': username,
        'username': username,
    }
    token = await encode_jwt(jwt_payload)
    return {"Authorization": f"Bearer {token}"}
