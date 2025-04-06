from aiogram import executor
from loader import dp, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.webinar_utils import send_webinar_reminders
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def on_startup(dispatcher):
    # Komandalarni sozlash
    await set_default_commands(dispatcher)

    # Adminlarga xabar
    await on_startup_notify(dispatcher)

    # 🔁 Reminder scheduler start
    scheduler.add_job(send_webinar_reminders, 'interval', minutes=1, args=[bot])
    scheduler.start()
    print("✅ Reminder scheduler started.")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
