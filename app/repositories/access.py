from fastapi import Depends
from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AccessType, TaskAccess
from app.db.db import get_db


class AccessRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, task_id: int, user_id: int):
        stmt = select(TaskAccess).where(and_(TaskAccess.task_id == task_id, TaskAccess.user_id == user_id))

        access = await self.db.execute(stmt)
        access = access.scalar()

        return access

    async def get_access_id(self, access_type: str):
        stmt = select(AccessType.id).where(AccessType.type == access_type)

        access_id = await self.db.execute(stmt)
        access_id = access_id.scalar()

        return access_id

    async def create_access(self, task_id: int, user_id: int, access_id: int):
        access = TaskAccess(
            task_id=task_id,
            user_id=user_id,
            access_id=access_id

        )
        self.db.add(access)

    async def update_access(self, task_id: int, user_id: int, access_id: int):
        stmt = update(TaskAccess).where(and_(TaskAccess.task_id == task_id, TaskAccess.user_id == user_id)).values(
            access_id=access_id
        )

        await self.db.execute(stmt)

    async def delete_access(self, access: TaskAccess):
        await self.db.delete(access)

    async def check_access(self, task_id: int, user_id: int):
        stmt = (
            select(AccessType.type)
            .select_from(AccessType)
            .join(TaskAccess, AccessType.id == TaskAccess.access_id)
            .where(
                and_(
                    TaskAccess.task_id == task_id,
                    TaskAccess.user_id == user_id,
                )
            )
        )
        access = await self.db.execute(stmt)
        access = access.scalar()

        return access
