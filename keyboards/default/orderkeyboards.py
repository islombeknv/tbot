from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

data = requests.get('https://papayes.cf/category/').json()

but = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, )
but.add(*(KeyboardButton(text=str(num['title'])) for num in data))
but.add(KeyboardButton(text='🏠 Bosh menyu'), KeyboardButton(text='⬅️ Orqaga'))

ordbut = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💳 Click'),
            KeyboardButton(text='💵 Naqd')
        ],
        [
            KeyboardButton(text='⬅️ Orqaga')
        ],
    ],
    resize_keyboard=True
)

delevery = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🏫 Olib ketish'),
            KeyboardButton(text='🛵 Yetkazib berish')
        ],
        [
            KeyboardButton(text='⬅️ Orqaga')
        ],
    ],
    resize_keyboard=True
)

checkbutton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅ Buyurtmani tasdiqlash')
        ],
        [
            KeyboardButton(text='💬 Buyurtmaga kommentariy')
        ],
        [
            KeyboardButton(text='⬅️ Orqaga'),
            KeyboardButton(text='❌ Bekor qilish')

        ],
    ],
    resize_keyboard=True
)

comback = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬅️ Orqaga')

        ],
    ],
    resize_keyboard=True
)

location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍Lokatsiya yuborish', request_location=True)

        ],
        [
            KeyboardButton(text='⬅️ Orqaga')

        ],
    ],
    resize_keyboard=True
)

number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📲 Telefon raqamni yuborish', request_contact=True)

        ],
        [
            KeyboardButton(text='⬅️ Orqaga')

        ],
    ],
    resize_keyboard=True
)