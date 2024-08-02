from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User
from app.db.db import get_db


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, username: str):
        user = await self.db.execute(select(User).where(User.username == username))
        user = user.scalar()
        return user

    async def get_by_id(self, user_id: int):
        user = await self.db.execute(select(User).where(User.id == user_id))
        user = user.scalar()
        return user

    async def get_username(self, user_id: int = None):
        user = await self.db.execute(select(User.username).where(User.id == user_id))
        user = user.scalar()
        return user

    async def create(self, user: User):
        self.db.add(user)
