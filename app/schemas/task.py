from datetime import datetime
from typing import Optional

from pydantic import field_serializer

from app.schemas.config import ConfigBaseModel


class TaskBase(ConfigBaseModel):
    pass


class TaskRead(TaskBase):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    status: str
    owner: str

    @field_serializer('created_at', 'updated_at')
    @staticmethod
    def format_datetime(value):
        return value.strftime("%H:%M:%S %d-%m-%Y")


class TaskCreate(TaskBase):
    title: str
    description: str


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
