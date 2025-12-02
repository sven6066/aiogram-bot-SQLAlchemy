from aiogram_dialog import Dialog

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Next, Back, Button
from aiogram_dialog.widgets.text import Const, Format


class AddCar(StatesGroup):
    choice_server = State()
    choice_method_select_contract = State()
    choice_contract_id = State()
    choice_contract_name = State()

choice_server = Window(
    Const("Выбери сервер братуха"),
    Format("Нажми далее бразе"),
    # Button(Const("Воронеж блейд"), on_click={lambda :}),
    # Button(Const("Москва блейд")),
    # Button(Const("Москва флойд"))
    Next(Const("далее")),
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