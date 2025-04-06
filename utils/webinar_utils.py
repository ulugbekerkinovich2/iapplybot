import json
from datetime import datetime, timedelta
from pathlib import Path
from aiogram import Bot

WEBINAR_TIME = datetime(2025, 3, 28, 11, 10)
WEBINAR_JSON = "data/webinar_users.json"
WEBINAR_LINK = "https://t.me/iapplyorguz/13"


REMINDER_MESSAGES = {
    "uz": {
        "1d": "📅 Eslatma: Webinar ertaga bo‘lib o‘tadi. Ishtirok etishga tayyorlaning!",
        "10m": f"🚀 Webinar 10 daqiqadan so‘ng boshlanadi!\n\n🔗 Kirish: {WEBINAR_LINK}"
    },
    "en": {
        "1d": "📅 Reminder: The webinar is tomorrow. Please get ready!",
        "10m": f"🚀 The webinar starts in 10 minutes!\n\n🔗 Join: {WEBINAR_LINK}"
    }
}

def save_user_to_webinar(user_data: dict):
    Path("data").mkdir(exist_ok=True)
    data = []

    if Path(WEBINAR_JSON).exists():
        with open(WEBINAR_JSON, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(user_data)

    with open(WEBINAR_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_webinar_countdown():
    now = datetime.now()
    delta = WEBINAR_TIME - now

    if delta.total_seconds() <= 0:
        return f"✅ Webinar boshlandi yoki tugadi.\n\n🔗 Webinar havolasi: {WEBINAR_LINK}"

    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes = rem // 60

    return (
        f"📅 Webinar sanasi: {WEBINAR_TIME.strftime('%d-%m-%Y, %H:%M')}\n"
        f"⏳ Qolgan vaqt: {days} kun {hours} soat {minutes} minut\n\n"
        f"🔗 Webinar havolasi: {WEBINAR_LINK}"
    )


async def send_webinar_reminders(bot: Bot):
    now = datetime.now()
    delta = WEBINAR_TIME - now
    minutes_left = int(delta.total_seconds() / 60)

    if minutes_left in [1440, 10]:
        if Path(WEBINAR_JSON).exists():
            with open(WEBINAR_JSON, "r") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []

            for user in users:
                try:
                    lang = user.get("lang", "uz")
                    if minutes_left == 1440:
                        await bot.send_message(user["id"], REMINDER_MESSAGES[lang]["1d"])
                    elif minutes_left == 10:
                        await bot.send_message(user["id"], REMINDER_MESSAGES[lang]["10m"])
                except:
                    continue


# async def notify_all_webinar_users(bot: Bot, message_text: str):
#     if Path(WEBINAR_JSON).exists():
#         with open(WEBINAR_JSON, "r") as f:
#             try:
#                 users = json.load(f)
#             except json.JSONDecodeError:
#                 users = []

#         for user in users:
#             try:
#                 await bot.send_message(user["id"], message_text)
#             except:
#                 continue
