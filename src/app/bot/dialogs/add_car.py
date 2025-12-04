import operator
from typing import Any
from dishka import FromDishka, AsyncContainer

from aiogram.fsm.context import FSMContext
from aiogram_dialog import Dialog, DialogManager
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput, MessageInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Next, Back, Button, Select, Column, Row, SwitchTo, Group
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import CONTAINER_NAME

from src.app.database.repo import ServerRepo
from src.app.services.services import fetch_contracts_by_id


class AddCar(StatesGroup):
    select_server = State()
    select_method_contract = State()
    input_contract_id = State()
    input_contract_name = State()
    select_from_contract_list = State()
    input_gos_number = State()


async def _get_server(dialog_manager:DialogManager, **kwargs):
    container: AsyncContainer = dialog_manager.middleware_data[CONTAINER_NAME]
    server_repo = await container.get(ServerRepo)
    servers = await server_repo.get_servers()
    return {
        "servers": [(server.name, server.id) for server in servers],
    }

async def _get_state_data(dialog_manager: DialogManager, **kwargs):
    container: AsyncContainer = dialog_manager.middleware_data[CONTAINER_NAME]
    server_repo = await container.get(ServerRepo)

    server_id = dialog_manager.dialog_data.get("server_id")
    if server_id:
        server = await server_repo.get_server(server_id)
        if server:
            dialog_manager.dialog_data["server_name"] = server.name

    return {
        "server_name": dialog_manager.dialog_data.get("server_name", None),
        "error_msg": dialog_manager.dialog_data.get("error_msg", None),
    }

async def _clear_error_data(callback:CallbackQuery, button:Button, manager: DialogManager, **kwargs):
    manager.dialog_data.pop("error_msg", None)

async def _on_server_selected(callback: CallbackQuery, widget: Any,
                              manager: DialogManager, item_id: str, ):
    server_id = int(item_id)
    manager.dialog_data["server_id"] = server_id
    # Очищаем старое имя сервера на случай, если пользователь вернулся назад и выбрал другой
    manager.dialog_data.pop("server_name", None)
    await manager.next()

select_server = Window(
    Const("Выбери сервер братуха"),
    Column(
        Select(
            Format("{item[0]}"),
            id="server",
            item_id_getter=operator.itemgetter(1),
            items="servers",
            on_click=_on_server_selected,
        )
    ),
    getter=_get_server,
    state=AddCar.select_server,
)

select_method_contract = Window(
    Format("Выбран сервер: {server_name}\nВыбери метод выбора договора"),
    Group(
        Row(
            SwitchTo(
                Const("🆔 По ID"),
                id="method_id",
                state=AddCar.input_contract_id
            ),
            SwitchTo(
                Const("🔤 По Названию"),
                id="method_id",
                state=AddCar.input_contract_name
            )
        ),
        Back(Const("назад")),
    ),
    getter=_get_state_data,
    state=AddCar.select_method_contract,
)

def _contract_id_validator(text: str):
    if not text.isdigit():
        raise ValueError("ID должен состоять только из цифр")
    return text

async def _on_id_error(message: Message, widget: ManagedTextInput, manager: DialogManager, error_: ValueError):
    manager.dialog_data["error_msg"] = f"Ошибка {error_}"

async def _on_id_success(message: Message, widget: ManagedTextInput, manager: DialogManager, data: str):
    container: AsyncContainer = manager.middleware_data[CONTAINER_NAME]
    server_repo = await container.get(ServerRepo)

    contract_id = data
    server_id = manager.dialog_data.get("server_id")
    contract = await fetch_contracts_by_id(server_id, contract_id, server_repo) #todo ВАЖНО создать нужно убрать передачу объекта подключения к бд, и создавать её самим
    if contract:
        manager.dialog_data["contract_id"] = contract_id
        manager.dialog_data["contract_name"] = contract.get("org_name")
        manager.dialog_data.pop("error_msg", None)
        await message.answer(f"Найден договор: {contract.get('org_name')}") # todo временно вывод ид договора
    else:
        manager.dialog_data["error_msg"] = f"Договор с ID {contract_id} не найден."
    # manager.dialog_data["contract_id"] = data
    # await message.answer(f"Вы ввели {data}")
    # await manager.switch_to(AddCar.input_gos_number)


input_contract_id = Window(
    Const("Введите ID договора: "),
    Format("{dialog_data[error_msg]}", when="error_msg"),
    TextInput(
        id="input_id_handler",
        type_factory=_contract_id_validator,
        on_success=_on_id_success,
        on_error=_on_id_error
    ),
    Back(
        Const("Назад"),
        on_click=  _clear_error_data,
    ),
    getter=_get_state_data,
    state=AddCar.input_contract_id
)

input_gos_number=Window(
    Const("Введите Гос. Номер ТС (пример: АС 154 А 36): "),
    state=AddCar.input_gos_number
)

main_dialog = Dialog(
    select_server,
    select_method_contract,
    input_contract_id
)
