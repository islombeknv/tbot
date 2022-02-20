from keyboards.default.newkeyboards import settings, menu
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from states.commentState import CommentData


@dp.message_handler(text='✍ Оставить отзыв', state=None)
async def com_test(message: types.Message):
    await message.answer('Izoh kiriting', reply_markup=settings)
    await CommentData.comment.set()


@dp.message_handler(state=CommentData.comment)
async def comment(message: types.Message, state: FSMContext):
    user_com = message.text
    await state.update_data(
        {'user_com': user_com}
    )

    data = await state.get_data()
    comm = data.get("user_com")

    await state.finish()

    await message.answer('Izohingiz qabul qilindi ', reply_markup=menu)
    # await StartState.start.set()