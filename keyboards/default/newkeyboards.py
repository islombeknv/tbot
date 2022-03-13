from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='🍔 Buyurtma berish')
            ],
            [
                KeyboardButton(text='🛒 Korzina'),
                KeyboardButton(text='📦 Buyurtmalarim'),
            ],
            [
                KeyboardButton(text='👨🏻‍💻 Admin'),
                KeyboardButton(text='⚙ Sozlamalar')
            ]
        ],
        resize_keyboard=True
    )

menu_rus = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='🍔 Заказать')
            ],
            [
                KeyboardButton(text='🛒 Корзина'),
                KeyboardButton(text='📦 Мои заказы'),
            ],
            [
                KeyboardButton(text='👨🏻‍💻 Админ'),
                KeyboardButton(text='⚙ Настройки')
            ]
        ],
        resize_keyboard=True
    )