import logging

import requests
from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    data = requests.get(f'https://papayes.cf/user/').json()
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Admin Bot qayta ishga tushdi")

        except Exception as err:
            logging.exception(err)
    # for user in data:
    #     try:
    #         await dp.bot.send_message(user['tg_id'], "Bot qayta ishga tushdi iltimos /start ni"
    #                                                  " bosing aks holda bot to\'liq ishlamaydi")
    #
    #     except Exception as err:
    #         logging.exception(err)
