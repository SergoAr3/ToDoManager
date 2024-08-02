from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class TaskAccess(Base):
    __tablename__ = 'task_access'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    access_id: Mapped[int] = mapped_column(ForeignKey('access_type.id', ondelete='CASCADE'), nullable=False,
                                           index=True)
