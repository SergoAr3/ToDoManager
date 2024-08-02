from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class AccessType(Base):
    __tablename__ = 'access_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)


