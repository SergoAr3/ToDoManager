from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.utils import encode_jwt, validate_auth_user
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services.auth import AuthService

auth_router = APIRouter()


@auth_router.post('/register', status_code=status.HTTP_204_NO_CONTENT)
async def register(
        user: UserCreate,
        auth_service: Annotated[AuthService, Depends()],
):
    reg_user = await auth_service.create_user(user)
    if reg_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User with this username already exists!')


@auth_router.post('/login', response_model=Token)
async def login_access_token(
        user: UserCreate = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
    }
    token = await encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer"
    )
