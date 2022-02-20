import requests
from datetime import datetime
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.default.newkeyboards import menu, settings
from keyboards.default.orderkeyboards import but, ordbut, delevery, checkbutton, comback
from keyboards.inline.utils import my_callback
from data.config import ADMINS
from loader import dp
from save import save_user
from states.orderState import OrderData, RegOrderData


@dp.message_handler(Command('start'))
async def show_menu(message: Message):
    await message.answer(f"Assalomu aleykum {message.from_user.full_name}", reply_markup=menu)
    if save_user(message) == 201:
        join = datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%Y-%m-%d, %H:%M')
        for admin in ADMINS:
            txt = f"Yangi foydalanuvchi qo'shildi:\n" \
                  f"<b>Vaqti:</b> {join}\n" \
                  f"<b>User:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
            await dp.bot.send_message(admin, txt, parse_mode='HTML')


@dp.message_handler(CommandStart(), state=OrderData)
async def show_menu(message: Message, state: FSMContext):
    await message.answer(f"Assalomu alekum {message.from_user.full_name}", reply_markup=menu)
    await state.finish()


@dp.message_handler(text='🍔 Buyurtma berish')
async def show_menu(message: Message):
    await message.answer(f"Categories", reply_markup=but)
    await OrderData.category.set()


@dp.message_handler(text='📦 Buyurtmalarim')
async def show_menu(message: Message):
    await message.answer(f"Вы совсем ничего не заказали.", reply_markup=menu)


@dp.message_handler(text='⚙ Настройки')
async def show_menu(message: Message):
    await message.answer(f"Настройки временно не доступны", reply_markup=settings)


@dp.message_handler(text='🛒 Korzina')
async def show_menu(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=3, )
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    x = 0
    txt = f'🛒Savatdagi mahsulotlar\n\n'
    for i in data:
        txt += f'🔹<b>{i["product"]}</b>\n' \
               f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,} \n\n'
        x += i["price"] * int(i["count"])
    txt += f'<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')

    keyboard.row(*(types.InlineKeyboardButton(f'✖️{i["product"]}',
                                              callback_data=my_callback.new(item=f'id_{i["id"]}')) for i in data))
    keyboard.add(types.InlineKeyboardButton('♻️Tozalash', callback_data=my_callback.new(item='clear')))
    keyboard.add(types.InlineKeyboardButton('✅ Rasmiylashtirish', callback_data=my_callback.new(item='order')))
    if data:
        await message.answer(txt, reply_markup=keyboard, parse_mode='HTML')
    else:
        await message.answer('Korzina bo\'sh, Mahsulotlarni tanlang va korzinaga qo\'shing', reply_markup=but,
                             reply=True)
        await OrderData.category.set()


@dp.callback_query_handler(my_callback.filter(item='clear'))
async def korzinaclear(call: CallbackQuery, callback_data: dict):
    requests.get(url=f'http://127.0.0.1:8000/korzina/clear/{call.from_user.id}')
    await dp.bot.edit_message_text(text='🛒 Korzina tozalandi', chat_id=call.message.chat.id,
                                   message_id=call.message.message_id)


@dp.callback_query_handler(my_callback.filter(item='order'))
async def order(call: CallbackQuery, callback_data: dict):
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{call.from_user.id}').json()
    if data:
        await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await dp.bot.send_message(chat_id=call.message.chat.id, text='To`lov turini tanlang', reply_markup=ordbut)
        await RegOrderData.pay.set()
    else:
        await call.answer(text="Korzina bo'sh", show_alert=True)


@dp.callback_query_handler(my_callback.filter())
async def korzina(call: CallbackQuery, callback_data: dict):
    pk = callback_data.get('item').split('_')[1]
    requests.delete(url=f'http://127.0.0.1:8000/korzina/delete/{pk}')
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{call.from_user.id}').json()
    x = 0
    txt = f'🛒Savatdagi mahsulotlar\n\n'
    for i in data:
        txt += f'🔹<b>{i["product"]}</b>\n' \
               f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,} \n\n'
        x += i["price"] * int(i["count"])
    txt += f'<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')

    keyboard.row(*(types.InlineKeyboardButton(f'✖️{i["product"]}',
                                              callback_data=my_callback.new(item=f'id_{i["id"]}')) for i in data))
    keyboard.add(types.InlineKeyboardButton('♻️Tozalash', callback_data=my_callback.new(item='clear')))
    keyboard.add(types.InlineKeyboardButton('✅Rasmiylashtirish', callback_data=my_callback.new(item='order')))
    try:
        await dp.bot.edit_message_text(text=txt, chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, reply_markup=keyboard)
    except:
        await dp.bot.edit_message_text(text='Korzina bo\'sh, Mahsulotlarni tanlang va korzinaga qo\'shing',
                                       chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, reply_markup=but)
        await OrderData.category.set()


@dp.message_handler(state=RegOrderData.pay)
async def regorder(message: Message, state: FSMContext):
    if message.text == '⬅️ Orqaga':
        await message.answer('🏠 Bosh menu', reply_markup=menu)
        await state.finish()
    elif message.text == '💳 Click':
        await state.update_data(
            {"pay": message.text}
        )
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()
    elif message.text == '💵 Naqd':
        await state.update_data(
            {"pay": message.text}
        )
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()


@dp.message_handler(state=RegOrderData.delivery)
async def regorder2(message: Message, state: FSMContext):
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    txt = ''
    x = 0
    for i in data:
        txt += f'<b>{i["product"]}</b>\n' \
               f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,}\n'
        x += i["price"] * int(i["count"])
    txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
    if message.text == '⬅️ Orqaga':
        await message.answer('To`lov turini yuboring', reply_markup=ordbut)
        await RegOrderData.pay.set()
    elif message.text == '🏫 Olib ketish':
        await state.update_data(
            {"delevery": message.text}
        )
        data = await state.get_data()
        pay = data.get("pay")
        delever = data.get("delevery")
        text = f"<b>Sizning buyurtmangiz</b>\nTo'lov:{pay}\nYetkazib berish:{delever}"
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()
    elif message.text == '🛵 Yetkazib berish':
        await state.update_data(
            {"delevery": message.text}
        )
        data = await state.get_data()
        pay = data.get("pay")
        delever = data.get("delevery")
        text = f"<b>Sizning buyurtmangiz</b>\nTo'lov:{pay}\nYetkazib berish:{delever}"
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()


@dp.message_handler(state=RegOrderData.location)
async def regorder2(message: Message, state: FSMContext):
    if message.text == '⬅️ Orqaga':
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()

    elif message.text == '💬 Buyurtmaga kommentariy':
        text = f"Izoh kiriting"
        await message.answer(text, reply_markup=comback)
        await RegOrderData.comment.set()


@dp.message_handler(state=RegOrderData.comment)
async def regorder3(message: Message, state: FSMContext):
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    txt = ''
    x = 0
    for i in data:
        txt += f'<b>{i["product"]}</b>\n' \
               f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,}\n'
        x += i["price"] * int(i["count"])
    txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
    data = await state.get_data()
    pay = data.get("pay")
    delever = data.get("delevery")
    text = f"<b>Sizning buyurtmangiz</b>\nTo'lov:{pay}\nYetkazib berish:{delever}\n"
    if message.text == '⬅️ Orqaga':
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()
    else:
        await state.update_data(
            {"comment": message.text}
        )
        await message.answer(f'{text}<b>Izoh</b>: {message.text}\n\n{txt}', reply_markup=checkbutton)
        await RegOrderData.location.set()