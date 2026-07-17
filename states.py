from aiogram.fsm.state import State, StatesGroup


class PaymentState(StatesGroup):
    amount = State()
    photo = State()


class OrderState(StatesGroup):
    service = State()
    link = State()
    quantity = State()