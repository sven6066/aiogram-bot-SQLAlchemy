from typing import Optional
from .endpoints import AdminApi,ClientApi

import aiohttp


class ServerNode:
    """
    Класс-обертка для одного конкретного сервера.
    Управляет жизненным циклом aiohttp сессии.
    """

    def __init__(self, admin_url: str, client_url: str):
        self.admin_url = admin_url
        self.client_url = client_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.admin: Optional[AdminApi] = None
        self.client: Optional[ClientApi] = None

    async def __aenter__(self):
        # Создаем сессию при входе в контекстный менеджер (async with)
        # CookieJar создается автоматически
        self.session = aiohttp.ClientSession()
        self.admin = AdminApi(self.session, self.admin_url)
        self.client = ClientApi(self.session, self.client_url)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Обязательно закрываем сессию при выходе
        if self.session:
            await self.session.close()

    async def authorize_client_as_admin(self, target_user_id: int):
        """
        Бизнес-логика: 'Админ заходит как клиент'
        """
        print(f"--- Начинаем процесс Impersonation на сервере {self.admin_url} и {self.client_url} ---")

        # 1. Админ получает одноразовый токен
        temp_token = await self.admin.get_impersonation_token(target_user_id)

        # 2. Клиентская часть обменивает токен на полноценную сессию (куки)
        await self.client.login_via_token(temp_token)
        print("--- Impersonation завершен ---")