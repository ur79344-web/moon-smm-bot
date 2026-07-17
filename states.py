from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    waiting_service = State()
    waiting_link = State()
    waiting_quantity = State()
