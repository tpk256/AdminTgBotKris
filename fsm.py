from aiogram.fsm.state import StatesGroup, State


class ClientConfigState(StatesGroup):
    choosing_name_client = State()
