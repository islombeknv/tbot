import requests
from datetime import datetime
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.default.newkeyboards import menu, menu_rus
from keyboards.default.orderkeyboards import but, ordbut, delevery, checkbutton, comback, location, number, but_rus, \
    ordbut_rus
from keyboards.inline.lang import langs
from keyboards.inline.mycallbak import ordcallback
from keyboards.inline.utils import my_callback
from data.config import ADMINS
from loader import dp
from save import save_user, Create_order
from states.orderState import OrderData, RegOrderData
from utils.location import get_address_from_coords

users = dict()


@dp.message_handler(Command('start'))
async def show_menu1(message: Message):
    users[message.from_user.id] = dict()
    await dp.bot.send_message(message.chat.id, "Welcome to Papayes", reply_markup=ReplyKeyboardRemove())
    await dp.bot.send_message(message.chat.id, "Tilni tanlang | Выберите язык", reply_markup=langs)
    if save_user(message) == 201:
        join = datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%Y-%m-%d, %H:%M')
        for admin in ADMINS:
            txt = f"Yangi foydalanuvchi qo'shildi:\n" \
                  f"<b>Vaqti:</b> {join}\n" \
                  f"<b>User:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
            await dp.bot.send_message(admin, txt, parse_mode='HTML')


@dp.callback_query_handler(text=['uzb', 'rus'])
async def myorder(call: CallbackQuery):
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'uzb':
        users[call.from_user.id]['lang'] = 'uzb'
        await dp.bot.send_message(call.message.chat.id, f"Assalomu alekum {call.from_user.full_name}",
                                  reply_markup=menu)
    elif call.data == 'rus':
        users[call.from_user.id]['lang'] = 'rus'
        await dp.bot.send_message(call.message.chat.id, f"Ассалому алекум {call.from_user.full_name}",
                                  reply_markup=menu_rus)


@dp.message_handler(CommandStart(), state=OrderData)
async def show_menu2(message: Message, state: FSMContext):
    await state.finish()
    lang = users[message.from_user.id].get('lang', '-')
    if lang == 'rus':
        await message.answer(f"Ассалому алекум {message.from_user.full_name}", reply_markup=menu_rus)
    else:
        await message.answer(f"Assalomu alekum {message.from_user.full_name}", reply_markup=menu)


@dp.message_handler(CommandStart(), state=RegOrderData)
async def show_menu3(message: Message, state: FSMContext):
    await state.finish()
    lang = users[message.from_user.id].get('lang', '-')
    if lang == 'rus':
        await message.answer(f"Ассалому алекум {message.from_user.full_name}", reply_markup=menu_rus)
    else:
        await message.answer(f"Assalomu alekum {message.from_user.full_name}", reply_markup=menu)


@dp.message_handler(text=['🍔 Buyurtma berish', '🍔 Заказать'])
async def show_menu4(message: Message):
    lang = users[message.from_user.id].get('lang', '-')
    if lang == 'rus':
        await message.answer('Категории', reply_markup=but_rus)
    else:
        await message.answer('Kategoriyalar', reply_markup=but)
    await OrderData.category.set()


@dp.message_handler(text=['📦 Buyurtmalarim', '📦 Мои заказы'])
async def Order(message: Message):
    keyboard = types.InlineKeyboardMarkup()
    data = requests.get(f'http://127.0.0.1:8000/order/{message.from_user.id}/').json()

    try:
        if data:
            if data['page_number'] != data['count'] and data['page_number'] == 1:
                keyboard.add(types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'),
                             types.InlineKeyboardButton('➡️',
                                                        callback_data=ordcallback.new(num=data['page_number'] + 1)))
            elif data['page_number'] != data['count'] and data['page_number'] != 1:
                keyboard.add(
                    types.InlineKeyboardButton('⬅️', callback_data=ordcallback.new(num=data['page_number'] - 1)),
                    types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'),
                    types.InlineKeyboardButton('➡️', callback_data=ordcallback.new(num=data['page_number'] + 1)))
            elif data['count'] == 1:
                keyboard.add(types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'))
            elif data['page_number'] == data['count']:
                keyboard.add(
                    types.InlineKeyboardButton('⬅️', callback_data=ordcallback.new(num=data['page_number'] - 1)),
                    types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'))

            lang = users[message.from_user.id].get('lang', '-')
            if lang == 'rus':
                await message.answer(f'ID: {data["results"][0]["id"]}\n'
                                     f'Время: {data["results"][0]["created_at"]}\n'
                                     f'Телефон: {data["results"][0]["number"]}\n'
                                     f'Расходы: {data["results"][0]["price"]}\n'
                                     f'\nУсловие: {data["results"][0]["order"]}',
                                     reply_markup=keyboard)

            else:
                await message.answer(f'ID: {data["results"][0]["id"]}\n'
                                     f'Vaqti: {data["results"][0]["created_at"]}\n'
                                     f'Telefon: {data["results"][0]["number"]}\n'
                                     f'Narxi: {data["results"][0]["price"]}\n'
                                     f'\nHolati: {data["results"][0]["order"]}',
                                     reply_markup=keyboard)

    except:
        await message.answer('Sizda buyurtmalar yo\'q | У вас нет заказов')


@dp.callback_query_handler(ordcallback.filter())
async def myorder(call: CallbackQuery, callback_data: dict):
    data = requests.get(f'http://127.0.0.1:8000/order/{call.from_user.id}/?page={callback_data.get("num")}').json()
    keyboard = types.InlineKeyboardMarkup()

    if data:
        try:
            if data['page_number'] == 1:
                keyboard.add(types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'),
                             types.InlineKeyboardButton('➡️',
                                                        callback_data=ordcallback.new(num=data['page_number'] + 1)))
            elif data['page_number'] != data['count'] and data['page_number'] != 1:
                keyboard.add(
                    types.InlineKeyboardButton('⬅️', callback_data=ordcallback.new(num=data['page_number'] - 1)),
                    types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'),
                    types.InlineKeyboardButton('➡️', callback_data=ordcallback.new(num=data['page_number'] + 1)))

            elif data['page_number'] == data['count']:
                keyboard.add(
                    types.InlineKeyboardButton('⬅️', callback_data=ordcallback.new(num=data['page_number'] - 1)),
                    types.InlineKeyboardButton(f"{data['page_number']} / {data['count']}", callback_data='0'))
            lang = users[call.from_user.id].get('lang', '-')
            if lang == 'rus':
                await dp.bot.edit_message_text(text=f'ID: {data["results"][0]["id"]}\n'
                                                    f'Время: {data["results"][0]["created_at"]}\n'
                                                    f'Телефон: {data["results"][0]["number"]}\n'
                                                    f'Расходы: {data["results"][0]["price"]}\n'
                                                    f'\nУсловие: {data["results"][0]["order"]}',
                                               chat_id=call.message.chat.id,
                                               message_id=call.message.message_id, reply_markup=keyboard)

            else:
                await dp.bot.edit_message_text(text=f'ID: {data["results"][0]["id"]}\n'
                                                    f'Vaqti: {data["results"][0]["created_at"]}\n'
                                                    f'Telefon: {data["results"][0]["number"]}\n'
                                                    f'Narxi: {data["results"][0]["price"]}\n'
                                                    f'\nHolati: {data["results"][0]["order"]}',
                                               chat_id=call.message.chat.id,
                                               message_id=call.message.message_id, reply_markup=keyboard)
        except:
            pass
    else:
        await call.answer('Sizda buyurtmalar yo\'q | У вас нет заказов')


@dp.message_handler(text=['⚙ Настройки', '⚙ Sozlamalar'])
async def settings(message: Message):
    lang = users[message.from_user.id].get('lang', '-')
    if lang == 'rus':
        await message.answer("Выберите язык", reply_markup=langs)
    else:
        await message.answer("Tilni tanlang", reply_markup=langs)


@dp.message_handler(text=['🛒 Korzina', '🛒 Корзина'])
async def show_menu6(message: Message):
    but_uz = types.InlineKeyboardMarkup(row_width=3, )
    but_ru = types.InlineKeyboardMarkup(row_width=3, )
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    x = 0
    txt = f'🛒Savatdagi mahsulotlar\n\n'
    txt_rus = f'🛒Товары в корзине\n\n'
    for i in data:
        txt += f'🔹<b>{i["product"]}</b>\n' \
               f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,} \n\n'
        x += i["price"] * int(i["count"])
        txt_rus += f'🔹<b>{i["product"]}</b>\n' \
                   f'{i["count"]} x {i["price"]} = {int(i["price"]) * int(i["count"]):,} \n\n'
    txt += f'<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
    txt_rus += f'<b>Общий:</b> {x:,} sum'.replace(',', ' ')

    but_uz.row(*(types.InlineKeyboardButton(f'✖️{i["product"]}',
                                            callback_data=my_callback.new(item=f'id_{i["id"]}')) for i in data))
    but_uz.add(types.InlineKeyboardButton('♻️Tozalash', callback_data=my_callback.new(item='clear')))
    but_uz.add(types.InlineKeyboardButton('✅ Rasmiylashtirish', callback_data=my_callback.new(item='order')))

    but_ru.row(*(types.InlineKeyboardButton(f'✖️{i["product"]}',
                                            callback_data=my_callback.new(item=f'id_{i["id"]}')) for i in data))
    but_ru.add(types.InlineKeyboardButton('♻️Уборка', callback_data=my_callback.new(item='clear')))
    but_ru.add(types.InlineKeyboardButton('✅ Регистрация', callback_data=my_callback.new(item='order')))

    if data:
        lang = users[message.from_user.id].get('lang', '-')
        if lang == 'rus':
            await message.answer(txt_rus, reply_markup=but_ru, parse_mode='HTML')
        else:
            await message.answer(txt, reply_markup=but_uz, parse_mode='HTML')
    else:
        lang = users[message.from_user.id].get('lang', '-')
        if lang == 'rus':
            await message.answer('Корзина пуста, выберите товары и добавьте их в корзину', reply_markup=but_rus,
                                 reply=True)
        else:
            await message.answer('Korzina bo\'sh, Mahsulotlarni tanlang va korzinaga qo\'shing', reply_markup=but,
                                 reply=True)
        await OrderData.category.set()


@dp.callback_query_handler(my_callback.filter(item='clear'))
async def korzinaclear(call: CallbackQuery, callback_data: dict):
    requests.get(url=f'http://127.0.0.1:8000/korzina/clear/{call.from_user.id}')

    lang = users[call.from_user.id].get('lang', '-')
    if lang == 'rus':
        await dp.bot.edit_message_text(text='🛒 Корзина очищена', chat_id=call.message.chat.id,
                                       message_id=call.message.message_id)
    else:
        await dp.bot.edit_message_text(text='🛒 Korzina tozalandi', chat_id=call.message.chat.id,
                                       message_id=call.message.message_id)


@dp.callback_query_handler(my_callback.filter(item='order'))
async def order(call: CallbackQuery, callback_data: dict):
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{call.from_user.id}').json()
    if data:
        await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        lang = users[call.from_user.id].get('lang', '-')
        if lang == 'rus':
            await dp.bot.send_message(chat_id=call.message.chat.id, text='Выберите тип оплаты', reply_markup=ordbut_rus)
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text='To`lov turini tanlang', reply_markup=ordbut)
        await RegOrderData.pay.set()
    else:
        lang = users[call.from_user.id].get('lang', '-')
        if lang == 'rus':
            await call.answer(text="Корзина пуста", show_alert=True)
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
               f'{i["count"]} x {int(i["price"]):,} = {int(i["price"]) * int(i["count"]):,} \n\n'
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
        await message.answer('Telefon raqamingizni yuboring yoki kiriting Misol: +998991234567', reply_markup=number)
        await RegOrderData.number.set()
    elif message.text == '💵 Naqd':
        await state.update_data(
            {"pay": message.text}
        )
        await message.answer('Telefon raqamingizni yuboring yoki kiriting Misol: +998991234567', reply_markup=number)
        await RegOrderData.number.set()


@dp.message_handler(state=RegOrderData.number)
@dp.message_handler(content_types='contact', state=RegOrderData.number)
async def regordernum(message: Message, state: FSMContext):
    if message.text == '⬅️ Orqaga':
        await message.answer('To`lov turini yuboring', reply_markup=ordbut)
        await RegOrderData.pay.set()
    elif message.contact.phone_number:
        await state.update_data(
            {"number": message.contact.phone_number}
        )
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()
    elif len(message.text) == 12 or len(message.text) == 13:
        await state.update_data(
            {"number": message.text}
        )
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()
    else:
        await message.answer("Nomer xato!", reply_markup=number)
        await RegOrderData.number.set()


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
        await message.answer('Telefon raqamingizni yuboring yoki kiriting Misol: +998991234567', reply_markup=number)
        await RegOrderData.number.set()
    elif message.text == '🏫 Olib ketish':
        await state.update_data(
            {"delevery": message.text}
        )
        data = await state.get_data()
        pay = data.get("pay")
        delever = data.get("delevery")
        text = f"<b>Sizning buyurtmangiz</b>\nNomer:{data.get('number')}\nTo'lov:{pay}\nYetkazib berish:{delever}"
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()
    elif message.text == '🛵 Yetkazib berish':
        await state.update_data(
            {"delevery": message.text}
        )
        await message.answer(f'Manzilni kiriting, tekst yoki lokatsiya yuboring', reply_markup=location)
        await RegOrderData.location.set()


@dp.message_handler(content_types='location', state=RegOrderData.location)
@dp.message_handler(content_types='text', state=RegOrderData.location)
async def regorder2(message: Message, state: FSMContext):
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    date = datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%Y-%m-%d, %H:%M')
    if message.text == '⬅️ Orqaga':
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()

    elif message.text == '✅ Buyurtmani tasdiqlash':
        txt = ''
        x = 0
        product = ''
        price = 0
        for i in data:
            txt += f'<b>{i["product"]}</b>\n' \
                   f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}\n'
            x += i["price"] * int(i["count"])
            product += f'{i["product"]}: ' \
                       f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}, '
            price += i["price"] * int(i["count"])
        txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
        db = await state.get_data()
        pay = db.get("pay")
        num = db.get("number")
        delever = db.get("delevery")
        com = ''
        address = ''
        if db.get("comment"):
            com += f'\n<b>Izoh</b>: {db.get("comment")}'
        text = f"<b>Yangi buyurtma {date}</b>\n\n<b>User: </b> <a href='tg://user?id={message.from_user.id}'>" \
               f"{message.from_user.first_name}</a>\n" \
               f"Nomer:{num}\nTo'lov:{pay}\nYetkazib berish:{delever}\n{com}\n{txt}"

        if db.get("address"):
            text = f"<b>Yangi buyurtma  {date}</b>\n\n<b>User: </b><a href='tg://user?id={message.from_user.id}'>" \
                   f"{message.from_user.first_name}</a>\n" \
                   f"Nomer: {num}\nTo'lov: {pay}\n" \
                   f"Yetkazib berish: {delever}\nManzil: {db.get('address')}\n{com}\n{txt}"

        for admin in ADMINS:
            await dp.bot.send_message(admin, text, parse_mode='HTML')
            if db.get("latitude") and db.get("longitude"):
                await dp.bot.send_location(admin, latitude=db.get("latitude"), longitude=db.get("longitude"))

        Create_order(product, price, address, num, message.from_user.id)

        await message.answer("Buyurtma qabul qilindi! Tez orada siz bilan bog'lanamiz", reply_markup=menu)
        await state.finish()

    elif message.text == '❌ Bekor qilish':
        await message.answer("Buyurtma bekor qilindi", reply_markup=menu)
        await state.finish()

    elif message.text == '💬 Buyurtmaga kommentariy':
        await message.answer("Izoh kiriting", reply_markup=comback)
        await RegOrderData.comment.set()

    elif message.location:
        address = get_address_from_coords(f"{message.location.longitude}, {message.location.latitude},")
        await state.update_data(
            {
                "address": address,
                "longitude": message.location.longitude,
                "latitude": message.location.latitude,
            }
        )
        txt = ''
        x = 0
        for i in data:
            txt += f'<b>{i["product"]}</b>\n' \
                   f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}\n'
            x += i["price"] * int(i["count"])
        txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
        data = await state.get_data()
        pay = data.get("pay")
        num = data.get("number")
        delever = data.get("delevery")
        text = f"<b>Sizning buyurtmangiz</b>\nNomer:{num}\nTo'lov:{pay}\nYetkazib berish:{delever}\nManzil:{address}"
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()

    else:
        await state.update_data(
            {"address": message.text}
        )
        txt = ''
        x = 0
        for i in data:
            txt += f'<b>{i["product"]}</b>\n' \
                   f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}\n'
            x += i["price"] * int(i["count"])
        txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
        data = await state.get_data()
        pay = data.get("pay")
        num = data.get("number")
        delever = data.get("delevery")
        address = data.get("address")
        text = f"<b>Sizning buyurtmangiz</b>\nNomer:{num}\nTo'lov:{pay}\nYetkazib berish:{delever}\nManzil:{address}"
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()


@dp.message_handler(state=RegOrderData.comment)
async def regorder3(message: Message, state: FSMContext):
    await state.update_data(
        {"comment": message.text}
    )
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    txt = ''
    x = 0
    for i in data:
        txt += f'<b>{i["product"]}</b>\n' \
               f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}\n'
        x += i["price"] * int(i["count"])
    txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
    data = await state.get_data()
    pay = data.get("pay")
    delever = data.get("delevery")
    text = f"<b>Sizning buyurtmangiz</b>\nNomer:{data.get('number')}\nTo'lov:{pay}\nYetkazib berish:{delever}\n"
    if data.get("address"):
        text = f"<b>Sizning buyurtmangiz</b>\nNomer:{data.get('number')}\nTo'lov:{pay}\nYetkazib berish:{delever}\nManzil:{data.get('address')}\n"
    elif message.text == '⬅️ Orqaga':
        await message.answer(f'{text}\n\n{txt},', reply_markup=checkbutton)
        await RegOrderData.location.set()
    await message.answer(f'{text}\n<b>Izoh</b>: {data.get("comment")}\n\n{txt}', reply_markup=checkbutton)
    await RegOrderData.confirm.set()


@dp.message_handler(content_types='text', state=RegOrderData.confirm)
async def regorder4(message: Message, state: FSMContext):
    data = requests.get(f'http://127.0.0.1:8000/korzina/list/{message.from_user.id}').json()
    date = datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%Y-%m-%d, %H:%M')
    if message.text == '⬅️ Orqaga':
        await message.answer('Yetkazib berish turini tanlang', reply_markup=delevery)
        await RegOrderData.delivery.set()

    elif message.text == '✅ Buyurtmani tasdiqlash':
        txt = ''
        x = 0
        product = ''
        price = 0
        for i in data:
            txt += f'<b>{i["product"]}</b>\n' \
                   f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}\n'
            x += i["price"] * int(i["count"])
            product += f'{i["product"]}: ' \
                       f'{i["count"]} x {int(i["price"])} = {int(i["price"]) * int(i["count"]):,}, '
            price += i["price"] * int(i["count"])
        txt += f'\n<b>Umumiy:</b> {x:,} sum'.replace(',', ' ')
        db = await state.get_data()
        pay = db.get("pay")
        num = db.get("number")
        delever = db.get("delevery")
        com = ''
        address = ''
        if db.get("comment"):
            com += f'<b>Izoh</b>: {db.get("comment")}'
        text = f"<b>Yangi buyurtma {date}</b>\n\n<b>User: </b> <a href='tg://user?id={message.from_user.id}'>" \
               f"{message.from_user.first_name}</a>\n" \
               f"Nomer:{num}\nTo'lov:{pay}\nYetkazib berish:{delever}\n{com}\n{txt}"

        if db.get("address"):
            text = f"<b>Yangi buyurtma {date}</b>\n\n<b>User: </b><a href='tg://user?id={message.from_user.id}'>" \
                   f"{message.from_user.first_name}</a>\n" \
                   f"Nomer: {num}\nTo'lov: {pay}\n" \
                   f"Yetkazib berish: {delever}\nManzil: {db.get('address')}\n\n{com}\n\n{txt}"

        for admin in ADMINS:
            await dp.bot.send_message(admin, text, parse_mode='HTML')
            if db.get("latitude") and db.get("longitude"):
                await dp.bot.send_location(admin, latitude=db.get("latitude"), longitude=db.get("longitude"))

        Create_order(product, price, address, num, message.from_user.id)

        await message.answer("Buyurtma qabul qilindi! Tez orada siz bilan bog'lanamiz", reply_markup=menu)
        await state.finish()

    elif message.text == '❌ Bekor qilish':
        await message.answer("Buyurtma bekor qilindi", reply_markup=menu)
        await state.finish()

    elif message.text == '💬 Buyurtmaga kommentariy':
        await message.answer("Izoh kiriting", reply_markup=comback)
        await RegOrderData.comment.set()
