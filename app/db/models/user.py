from sqlalchemy import Boolean, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

