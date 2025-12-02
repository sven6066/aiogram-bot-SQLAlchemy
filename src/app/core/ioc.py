from typing import AsyncIterable

from aiogram.fsm import storage
from aiogram.fsm.storage.redis import RedisStorage
from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from src.app.database.repo import UserRepo
import os

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")


# Наш провайдер зависимостей
class DbProvider(Provider):

    # 1. Создаем Engine (Один раз на весь запуск бота)
    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        url = DATABASE_URL
        engine = create_async_engine(url, echo=True)
        yield engine
        await engine.dispose()  # Закроем при выключении бота

    # 2. Создаем фабрику сессий (Тоже одну на всё приложение)
    @provide(scope=Scope.APP)
    def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    # 3. Создаем СЕССИЮ (Для каждого запроса/сообщения)
    @provide(scope=Scope.REQUEST)
    async def get_session(self, maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with maker() as session:
            yield session

    # 4. Создаем РЕПОЗИТОРИЙ (Для каждого запроса)
    # Dishka сама увидит, что UserRepo требует session, и возьмет её из метода выше
    @provide(scope=Scope.REQUEST)
    async def get_user_repo(self, session: AsyncSession) -> UserRepo:
        return UserRepo(session)


from aiogram.fsm.storage.base import DefaultKeyBuilder


class RedisProvider(Provider):

    @provide(scope=Scope.APP)
    async def create_redis_connection(self) -> AsyncIterable[Redis]:
        url = REDIS_URL
        redis = Redis.from_url(url)
        yield redis
        await redis.close()

    @provide(scope=Scope.APP)
    async def get_storage(self, redis: Redis) -> RedisStorage:
        storage = RedisStorage(
            redis,
            key_builder=DefaultKeyBuilder(with_destiny=True)
        )
        return storage
