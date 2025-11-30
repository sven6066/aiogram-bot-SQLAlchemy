для запуска не обходимо:
- прогнать миграции `alembic revision --autogenerate -m "Initial migration"`
- создать таблицы из миграций `alembic upgrade head`
- запустить контейнер с ботом
