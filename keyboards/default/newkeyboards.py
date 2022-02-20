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

location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍 Отправьте геолокацию', request_location=True)
        ],
        [
            KeyboardButton(text='⬅ Orqaga')
        ],
    ],
    resize_keyboard=True
)

settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬅ Orqaga')
        ]
    ],
    resize_keyboard=True
)
