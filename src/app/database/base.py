import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# DATABASE_URL = os.getenv("DATABASE_URL")
#
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True
# )
# #Фабрика сессий. Через неё создаётся подключение в хендлерах.
# async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass