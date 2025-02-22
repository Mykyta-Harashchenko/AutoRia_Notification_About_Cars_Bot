from aiogram.fsm.state import StatesGroup, State


class FormAutoria(StatesGroup):
    title = State()