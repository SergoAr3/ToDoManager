from fastapi import Depends, HTTPException
from starlette import status

import app.api.constans as per

from app.db import Task, User
from app.repositories.access import AccessRepository
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(
            self,
            task_repository: TaskRepository = Depends(),
            user_repository: UserRepository = Depends(),
            access_repository: AccessRepository = Depends()
    ):
        self.task_repository = task_repository
        self.user_repository = user_repository
        self.access_repository = access_repository

    async def get_tasks(self, user: User):
        tasks = await self.task_repository.get_all(user.id)
        if tasks:
            res = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "status": task.status,
                    "owner": user.username

                } for task in tasks
            ]

            return res
        return []

    async def get_task(self, task_id: int, current_user_id: int):
        permission = per.EDITOR

        task = await self.task_exists(task_id)

        if task.owner_id != current_user_id:
            permission = await self.access_repository.check_access(task_id, current_user_id)

        if permission in [per.EDITOR, per.READ_ONLY]:
            owner_username = await self.user_repository.get(user_id=task.owner_id, get_username=True)
            res = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "status": task.status,
                "owner": owner_username
            }
            return res
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access denied")

    async def create_task(self, task_data: TaskCreate, user_id: int):
        task = Task(
            title=task_data.title,
            description=task_data.description,
            owner_id=user_id
        )
        await self.task_repository.create(task)

    async def update_task(self, task: TaskUpdate, task_id: int, current_user_id: int):
        permission = per.EDITOR
        db_task = await self.task_exists(task_id)

        if db_task.owner_id != current_user_id:
            permission = await self.access_repository.check_access(task_id, current_user_id)

        if permission in [per.EDITOR]:
            task_update_data = task.dict(exclude_unset=True)
            await self.task_repository.update(task_update_data, task_id)
            return
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access denied")

    async def delete_task(self, task_id: int, current_user_id):
        task = await self.task_exists(task_id)

        if task.owner_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Access denied")

        await self.task_repository.delete(task)
        return task

    async def assign_access(self, task_id: int, user_id: int, access: str, current_user_id: int):
        task = await self.task_exists(task_id)
        await self.user_exists(user_id)

        if task.owner_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Access denied")

        db_access = await self.access_repository.get(task_id, user_id)
        access_id = await self.access_repository.get_access_id(access)
        print(access_id)

        if db_access:
            await self.access_repository.update_access(task_id, user_id, access_id)
        else:
            await self.access_repository.create_access(task_id, user_id, access_id)

    async def revoke_access(self, task_id: int, user_id: int, current_user_id: int):
        task = await self.task_exists(task_id)
        await self.user_exists(user_id)

        if task.owner_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Access denied")

        access = await self.access_repository.get(task_id, user_id)
        if access:
            await self.access_repository.delete_access(access=access)
            return
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The user does not have access")

    async def task_exists(self, task_id: int):
        task = await self.task_repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    async def user_exists(self, user_id: int):
        task = await self.user_repository.get(user_id=user_id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return task
