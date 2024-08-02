from app.schemas.config import ConfigBaseModel


class UserBase(ConfigBaseModel):
    username: str
    password: str


class UserRead(UserBase):
    id: int
    active: bool = True


class UserCreate(UserBase):
    pass
