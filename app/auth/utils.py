from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.db import User
from app.repositories.user import UserRepository
from app.schemas.jwt import auth_jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)


async def validate_auth_user(
        user_repository: Annotated[UserRepository, Depends()],
        username: str = Form(),
        password: str = Form()
):
    unauth_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    user = await user_repository.get(username)
    if not user:
        raise unauth_exc
    if not await validate_password(
            password=password,
            hashed_password=user.hashed_password
    ):
        raise unauth_exc

    return user


async def encode_jwt(
        payload: dict,
        private_key: str = auth_jwt.private_key_path.read_text(),
        algorithm: str = auth_jwt.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = auth_jwt.access_token_expires_minutes
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode,
                         private_key,
                         algorithm=algorithm)
    return encoded


async def decode_jwt(
        jwt_token: str | bytes,
        public_key: str = auth_jwt.public_key_path.read_text(),
        algorithm: str = auth_jwt.algorithm

):
    decoded = jwt.decode(jwt_token, public_key, algorithms=[algorithm])
    return decoded


async def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )


async def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = await decode_jwt(
            jwt_token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
        user_repository: Annotated[UserRepository, Depends()],
        payload: dict = Depends(get_current_token_payload),
) -> User:
    username: str | None = payload.get("sub")
    user = await user_repository.get(username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
        user: User = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
