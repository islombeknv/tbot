import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.default.mahsulotSoni import mah_miqdori
from keyboards.default.newkeyboards import menu, menu_rus
from keyboards.default.orderkeyboards import but
from states.orderState import OrderData
from loader import dp, bot
from save import save_korzina
from handlers.users.start import users


@dp.message_handler(state=OrderData.category)
async def products(message: types.Message, state: FSMContext):
    lang = users[message.from_user.id].get('lang', '-')
    if message.text == '🏠 Bosh menyu' or message.text == '🏠 Главное меню':
        if lang == 'rus':
            await message.answer('🏠 Главное меню', reply_markup=menu_rus)
        else:
            await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()

    elif message.text == '⬅️ Orqaga' or message.text == '⬅️ Назад':
        if lang == 'rus':
            await message.answer('🏠 Главное меню', reply_markup=menu_rus)
        else:
            await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()
    try:
        data = requests.get(f'http://127.0.0.1:8000/category/{message.text}').json()
        if data:
            for x in data:
                keyboard_2 = []
                keyboard_2.append(
                    KeyboardButton(
                        text=f"{x['title']}"
                    )
                )
                prod_key = ReplyKeyboardMarkup(
                    keyboard=[
                        keyboard_2,
                        [
                            KeyboardButton(text='🏠 Bosh menyu'),
                            KeyboardButton(text='⬅ Orqaga')
                        ],
                    ],
                    resize_keyboard=True,
                    row_width=2
                )
                prod_key_rus = ReplyKeyboardMarkup(
                    keyboard=[
                        keyboard_2,
                        [
                            KeyboardButton(text='🏠 Главное меню'),
                            KeyboardButton(text='⬅️ Назад')
                        ],
                    ],
                    resize_keyboard=True,
                    row_width=2
                )
                await bot.send_chat_action(message.chat.id, 'typing')
                if lang == 'rus':
                    await message.answer('Продукты', reply_markup=prod_key_rus)
                else:
                    await message.answer('Mahsulotlar', reply_markup=prod_key)
                await OrderData.products.set()
    except:
        pass


@dp.message_handler(state=OrderData.products)
async def products_detail(message: types.Message, state: FSMContext):
    lang = users[message.from_user.id].get('lang', '-')
    photo = "https://kitoblardunyosi.uz/image/cache/catalog/001-Kitoblar/003_boshqalar/006_ilmiy_ommabop/python-3d-web-500x500h.jpg"
    detail_prod = requests.get(f'http://127.0.0.1:8000/product/?q={message.text}').json()
    if message.text == '🏠 Bosh menyu' or message.text == '🏠 Главное меню':
        if lang == 'rus':
            await message.answer('🏠 Главное меню', reply_markup=menu_rus)
        else:
            await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()

    elif message.text == '⬅ Orqaga':
        await message.answer('Categories', reply_markup=but)
        await OrderData.category.set()

    for y in detail_prod:
        if str(message.text) == str(y['title']):
            text = f"{y['title']}\n\n{y['description']}\n\nNarxi: {y['price']:,} sum"
            await message.answer_photo(photo=photo, caption=text)
            await message.answer('Miqdorini tanlang yoki kiriting', reply_markup=mah_miqdori)
            await OrderData.detail.set()
            await state.update_data(
                {
                    "title": y['title'],
                    "price": y['price']
                }
            )


@dp.message_handler(state=OrderData.detail)
async def products_detail(message: types.Message, state: FSMContext):
    try:
        if message.text == '🏠 Bosh menyu':
            await message.answer('🏠 Bosh menu', reply_markup=menu)
            await state.finish()

        elif message.text == '🛒 Korzina':
            await message.answer('🏠 Bosh menu', reply_markup=menu)
            await state.finish()
        elif int(message.text):
            data = await state.get_data()
            save_korzina(message, data.get("title"), data.get("price"), message.text)
            await message.answer('Mahsulot savatchaga qoshildi, davom etamizmi?', reply_markup=but)
            await OrderData.category.set()
    except:
        await message.answer('Siz noto\'g\'ri malimot kiritdingiz. Miqdorini tanlang yoki kiriting!')
