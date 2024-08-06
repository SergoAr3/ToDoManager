from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User
from app.db.db import get_db


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, username: str = None, user_id: int = None, get_username=False) -> User:
        if username:
            user = await self.db.scalar(select(User).filter_by(username=username))
            return user

        if get_username:
            user = await self.db.scalar(select(User.username).filter_by(id=user_id))
            return user

        user = await self.db.scalar(select(User.username).filter_by(id=user_id))
        return user

    async def create(self, user: User):
        self.db.add(user)
