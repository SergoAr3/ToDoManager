from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


load_dotenv()

engine = create_async_engine(getenv("DATABASE_URL"))
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
