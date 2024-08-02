from fastapi import Depends

from app.auth.utils import hash_password
from app.db import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate):
        hashed_password = await hash_password(user_data.password)
        user = await self.user_repository.get(user_data.username)
        if user is None:
            user = User(
                username=user_data.username,
                hashed_password=hashed_password
            )
            await self.user_repository.create(user)
            return
        return user
