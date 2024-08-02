from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Task
from app.db.db import get_db


class TaskRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, task_id: int):
        stmt = select(Task).where(Task.id == task_id)
        res = await self.db.execute(stmt)
        task = res.scalar()
        return task

    async def get_all(self, user_id: int):
        stmt = select(Task).where(Task.owner_id == user_id)
        res = await self.db.execute(stmt)
        tasks = res.scalars().all()
        return tasks

    async def create(self, task: Task):
        self.db.add(task)

    async def update(self, task_update_data: dict, task_id: int):
        stmt = (update(Task)
                .where(Task.id == task_id)
                .values(task_update_data))

        await self.db.execute(stmt)

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
