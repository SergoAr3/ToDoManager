from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Body, Query
from loguru import logger
from starlette import status

import app.api.errors as err
from app.auth.utils import get_current_active_auth_user
from app.db import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task import TaskService

tasks_router = APIRouter()


@tasks_router.get(
    '',
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "description": "Unauthorized"
        }
    },
    response_model=list[TaskRead]
)
async def get_all_tasks(
        task_service: Annotated[TaskService, Depends()],
        current_user: Annotated[User, Depends(get_current_active_auth_user)]
):
    try:
        tasks = await task_service.get_tasks(current_user)
        return tasks
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR


@tasks_router.get(
    '/{task_id}',
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Forbidden"
        },
        404: {
            "description": "Task not found"
        },
    },
    response_model=TaskRead
)
async def get_task(
        task_id: Annotated[int, Path()],
        task_service: Annotated[TaskService, Depends()],
        current_user: Annotated[User, Depends(get_current_active_auth_user)]
):
    try:
        task = await task_service.get_task(task_id, current_user.id)
        return task
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR


@tasks_router.post(
    '',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Task successfully created"
        },
        401: {
            "description": "Unauthorized"
        }
    }
)
async def create_task(
        task: Annotated[TaskCreate, Body()],
        task_service: Annotated[TaskService, Depends()],
        current_user: Annotated[User, Depends(get_current_active_auth_user)]

):
    try:
        await task_service.create_task(task, current_user.id)
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR


@tasks_router.patch(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Task successfully updated"
        },
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Forbidden"
        },
        404: {
            "description": "Task not found"
        },
    }
)
async def update_task(
        task_id: Annotated[int, Path()],
        task: Annotated[TaskUpdate, Body()],
        task_service: Annotated[TaskService, Depends()],
        current_user: User = Depends(get_current_active_auth_user),
):
    try:
        await task_service.update_task(task, task_id, current_user.id)
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR


@tasks_router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Task successfully deleted"
        },
        401: {
            "description": "Unauthorized"
        },
        404: {
            "description": "Task not found"
        },
    }
)
async def delete_task(
        task_id: Annotated[int, Path()],
        task_service: Annotated[TaskService, Depends()],
        current_user: User = Depends(get_current_active_auth_user),
):
    try:
        await task_service.delete_task(task_id, current_user.id)
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR


@tasks_router.post(
    '/{task_id}/access',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Access successfully assigned"
        },
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Forbidden"
        },
        404: {
            "description": "Task or User not found"
        },
    }
)
async def assign_access(
        task_id: Annotated[int, Path()],
        user_id: Annotated[int, Query()],
        access: Annotated[Literal['read only', 'editor'], Query()],
        task_service: Annotated[TaskService, Depends()],
        current_user: Annotated[User, Depends(get_current_active_auth_user)]
):
    try:
        await task_service.assign_access(task_id, user_id, access, current_user.id)
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR


@tasks_router.delete(
    '/{task_id}/access',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Access successfully revoked"
        },
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Forbidden"
        },
        404: {
            "description": "Task or User not found"
        },
    }
)
async def revoke_access(
        task_id: Annotated[int, Path()],
        user_id: Annotated[int, Query()],
        task_service: Annotated[TaskService, Depends()],
        current_user: Annotated[User, Depends(get_current_active_auth_user)]
):
    try:
        await task_service.revoke_access(task_id, user_id, current_user.id)
    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        logger.error(e)
        raise err.HTTP_500_INTERNAL_ERROR
