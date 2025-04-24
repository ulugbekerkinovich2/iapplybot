import logging
from aiogram import Dispatcher
from data.config import ADMINS

async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(chat_id=935920479, text="Bot ishga tushdi")
    except Exception as err:
        logging.exception(err)
