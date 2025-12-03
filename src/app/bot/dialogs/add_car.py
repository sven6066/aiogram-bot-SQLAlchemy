import operator
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram_dialog import Dialog, DialogManager

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Next, Back, Button, Select
from aiogram_dialog.widgets.text import Const, Format


class AddCar(StatesGroup):
    choice_server = State()
    choice_method_select_contract = State()
    choice_contract_id = State()
    choice_contract_name = State()

#todo хранить сервера в таблице бд
async def _get_server(**kwargs):
    servers = [
        ("Воронеж Блейд", 1),
        ("Москва Блейд", 2),
        ("Москва Флойд", 3)
    ]
    return {
        "servers": servers,
        # "count": len(servers)
    }

async def _on_server_selected(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id:str):
    context = manager.current_context()
    context.dialog_data["server_id"] = int(item_id)
    raw_servers = await _get_server()
    server_name = "Unknown"
    for name, s_id in raw_servers.get("servers"):
        if s_id == int(item_id):
            server_name = name
            break

    await callback.message.answer(f"Выбран сервер: {server_name}")
    await manager.next()

choice_server = Window(
    Const("Выбери сервер братуха"),

    Select(
        Format("сервер: {item[0]}"),
        id="server",
        item_id_getter=operator.itemgetter(1),
        items="servers",
        on_click=_on_server_selected,
    ),
    getter=_get_server,
    # Next(Const("далее")),
    state=AddCar.choice_server,
)

choice_contract = Window(
    Const("Выбери метод выбора договора"),
    Back(Const("назад")),
    Next(Const("далее")),
    state=AddCar.choice_method_select_contract,
)

main_dialog = Dialog(
    choice_server, choice_contract
)