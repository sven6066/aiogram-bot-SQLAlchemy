import os
from sqlite3.dbapi2 import paramstyle
from typing import Optional

import aiohttp


class AdminApi:
    def __init__(self, session: aiohttp.ClientSession, base_url: str):
        self._session = session
        self.base_url = base_url
        self._jwt_token: Optional[str] = None

    @property
    def _headers(self):
        """Динамически формируем заголовки. Если есть токен — добавляем его."""
        headers = {
            # "content-type":"application/x-www-form-urlencoded;"
        }
        if self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"
        return headers

    async def login(self, username:str = os.getenv("USERNAME_API"), password:str = os.getenv("PASSWORD_API")):
        """Сценарий 1: Авторизация админа по логину/паролю -> получаем JWT"""
        url = f"{self.base_url}backend/login.php"
        payload = {
            "username": username,
            "password": password,
            "cmd": "login",
        }

        async with self._session.post(url, data=payload, headers=self._headers) as resp:
            resp.raise_for_status()
            # print(await resp.text())
            # await resp.content.
            data = await resp.json(content_type=None)
            # Предполагаем, что сервер возвращает { "token": "..." }
            self._jwt_token = data.get("jwt_token")
            print(f"[Admin] Успешный вход на {self.base_url}")

    async def get_contracts(self):
        url = f"{self.base_url}/backend/app/accounts.php"
        params = {
            "cmd": "read",
            "sort": "id",
        }

        async with self._session.get(url, params=params, headers=self._headers) as resp:
            resp.raise_for_status()
            data = await resp.json(content_type=None)
            print("Успешный запрос получения договоров")
            return data

    async def get_impersonation_token(self, user_id: int) -> str:
        """Получение промежуточного токена для входа за пользователя"""
        if not self._jwt_token:
            raise Exception("Сначала нужно авторизоваться в админке!")

        url = f"{self.base_url}/api/admin/users/{user_id}/generate-token"

        async with self._session.post(url, headers=self._headers) as resp:
            resp.raise_for_status()
            data = await resp.json()
            # Сервер возвращает временный токен, например { "temp_auth_token": "xyz123" }
            return data.get("temp_auth_token")

    async def get_stats(self):
        """Пример защищенного метода админки"""
        url = f"{self.base_url}/api/admin/stats"
        async with self._session.get(url, headers=self._headers) as resp:
            return await resp.json()


class ClientApi:
    def __init__(self, session: aiohttp.ClientSession, base_url: str):
        self._session = session  # Эта сессия имеет свой CookieJar
        self.base_url = base_url

    async def login_direct(self, username, password):
        """Сценарий 2: Прямой вход клиента -> сессия сама запомнит куки"""
        url = f"{self.base_url}/api/client/login"
        payload = {"username": username, "password": password}

        async with self._session.post(url, json=payload) as resp:
            resp.raise_for_status()
            print(f"[Client] Прямой вход выполнен на {self.base_url}")
            # CookieJar внутри self._session автоматически сохранит куки из ответа

    async def login_via_token(self, temp_token: str):
        """Сценарий 3: Обмен промежуточного токена на куки"""
        # Обычно это GET или POST запрос, куда передается токен
        url = f"{self.base_url}/api/client/auth/exchange"
        payload = {"token": temp_token}

        async with self._session.post(url, json=payload) as resp:
            resp.raise_for_status()
            print(f"[Client] Вход через токен выполнен. Куки установлены.")
            # Сервер ответит Set-Cookie, aiohttp сохранит их для будущих запросов

    async def get_profile(self):
        """Пример метода клиента, требующего авторизации (куки)"""
        url = f"{self.base_url}/api/client/profile"
        async with self._session.get(url) as resp:
            return await resp.json()
