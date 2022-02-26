import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.default.mahsulotSoni import mah_miqdori
from keyboards.default.newkeyboards import menu
from keyboards.default.orderkeyboards import but
from states.orderState import OrderData
from loader import dp, bot
from save import save_korzina


@dp.message_handler(state=OrderData.category)
async def products(message: types.Message, state: FSMContext):
    if message.text == '🏠 Bosh menyu':
        await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()

    elif message.text == '⬅️ Orqaga':
        await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()
    await bot.send_chat_action(message.chat.id, 'typing')
    data = requests.get(f'https://papayes.cf/category/{message.text}').json()
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
            await message.answer('Mahsulotlar', reply_markup=prod_key)
            await OrderData.products.set()


@dp.message_handler(state=OrderData.products)
async def products_detail(message: types.Message, state: FSMContext):
    detail_prod = requests.get(f'https://papayes.cf/prod/?q={message.text}').json()
    if message.text == '🏠 Bosh menyu':
        await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()
    elif message.text == '⬅ Orqaga':
        await message.answer('Categories', reply_markup=but)
        await OrderData.category.set()

    await bot.send_chat_action(message.chat.id, 'typing')
    for y in detail_prod:
        if str(message.text) == str(y['title']):
            text = f"{y['title']}\n\n{y['description']}\n\nNarxi: {y['price']:,} sum"
            await message.answer_photo(photo=y['image'], caption=text)
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
