from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderData(StatesGroup):
    category = State()
    products = State()
    detail = State()
    order = State()


class RegOrderData(StatesGroup):
    pay = State()
    delivery = State()
    location = State()
    location1 = State()
    comment = State()
    confirm = State()
