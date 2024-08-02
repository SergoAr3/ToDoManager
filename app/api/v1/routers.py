from fastapi import FastAPI

from app.auth.handlers import auth_router
from .handlers import tasks_router

app = FastAPI(docs_url="/")

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    tasks_router,
    prefix="/task",
    tags=["Task"],
)

