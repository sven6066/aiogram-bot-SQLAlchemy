from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, telegram_id: int):
        # Проверяем, есть ли уже такой юзер (upsert логика может быть сложнее, но пока так)
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return existing_user

        # Если нет - создаем
        new_user = User(
            telegram_id=telegram_id
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)  # Обновляем объект (получаем его ID)
        return new_user

    async def __get_users_id(self):
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalar_one().telegram_id

    async def get_whitelist(self):
        stmt = select(User.telegram_id)
        result = await self.session.execute(stmt)
        # return result.scalar_one().telegram_id
        return set(result.scalars().all())