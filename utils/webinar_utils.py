import json
from datetime import datetime, timedelta
from pathlib import Path
from aiogram import Bot
import pytz
import asyncio
from keyboards.inline.user_inlineKeyboards import get_feedback_keyboard
from utils.lang import t
import asyncio
# from handlers.users.start import send_live_countdown

# tz = pytz.timezone("Asia/Tashkent")
# WEBINAR_TIME = tz.localize(datetime(2025, 4, 12, 10, 35))
tz = pytz.timezone("Asia/Tashkent")
# WEBINAR_TIME = tz.localize(datetime(2025, 4, 13, 18, 55))  # ✅ timezone-aware
now = datetime.now(tz)
# WEBINAR_TIME = datetime(2025, 4, 9, 20, 00)
WEBINAR_JSON = "data/webinar_users.json"
WEBINAR_LINK = "https://t.me/iapplyorguz/"
WEBINAR_FILE = WEBINAR_JSON

REMINDER_MESSAGES = {
    "uz": {
        "12h": "📅 Eslatma: Webinar 12 soatdan so'ng bo‘lib o‘tadi. Ishtirok etishga tayyorlaning!\n\n🔗 Kirish: {WEBINAR_LINK}",
        "180m": f"🚀 Webinar 3 soatdan so‘ng boshlanadi!\n\n🔗 Kirish: {WEBINAR_LINK}",
        "5m": f"🚀 Webinar 5 daqiqadan so'ng boshlanadi!\n\n🔗 Kirish: {WEBINAR_LINK}",
        "rate": "📊 Webinar sizga yoqdimi? 1–5 gacha baho bering:"
    },
    "en": {
        "12h": "📅 Reminder: The webinar starts in 12 hours. Please get ready!\n\n🔗 Join: {WEBINAR_LINK}",
        "180m": f"🚀 The webinar starts in 3 hours!\n\n🔗 Join: {WEBINAR_LINK}",
        "5h": f"🚀 The webinar starts in 5 minutes!\n\n🔗 Join: {WEBINAR_LINK}",
        "rate": "📊 Did you enjoy the webinar? Rate it from 1–5:"
    }
}

def save_user_to_webinar(user_data: dict):
    """
    Foydalanuvchini tegishli davlatdagi vebinar ro'yxatiga qo'shadi
    """
    user_id = user_data["id"]
    country = user_data.get("country")
    webinar_time = user_data.get("webinar_time", "")

    if not country:
        return

    # Fayl mavjud bo'lmasa, bo'sh dict yaratamiz
    if not Path(WEBINAR_FILE).exists():
        with open(WEBINAR_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    # Faylni o'qish
    with open(WEBINAR_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Agar davlat yo‘q bo‘lsa, yangi bo‘lim yaratamiz
    if country not in data:
        data[country] = {
            "datetime": webinar_time,
            "users": []
        }

    # Userga sent[] va boshqa zarur atributlar yo'q bo‘lsa, to‘ldiramiz
    if "sent" not in user_data:
        user_data["sent"] = []

    # User allaqachon ro'yxatda yo‘qligini tekshiramiz
    existing_ids = [u.get("id") for u in data[country]["users"]]
    if user_id not in existing_ids:
        data[country]["users"].append(user_data)

    # Faylni saqlaymiz
    with open(WEBINAR_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Globally define a set to remember already triggered minutes
# sent_minutes = set()

# async def send_webinar_reminders(bot: Bot):
#     now = datetime.now(tz)
#     delta = WEBINAR_TIME - now
#     minutes_left = int(delta.total_seconds() / 60)
#     print(minutes_left)
#     # 🔄 Faqat ijobiy vaqtlarda takrorlanmaslik uchun
#     if minutes_left in {1,2, 5, 180, 720, -1} and minutes_left not in sent_minutes:
#         sent_minutes.add(minutes_left)

#     # 🔁 JSONdan foydalanuvchilarni o‘qiymiz
#     if not Path(WEBINAR_JSON).exists():
#         return

#     with open(WEBINAR_JSON, "r", encoding="utf-8") as f:
#         try:
#             users = json.load(f)
#         except json.JSONDecodeError:
#             users = []

#     updated = False  # Faylni yangilash kerakmi, flag

#     for user in users:
#         try:
#             user_id = user["id"]
#             lang = user.get("lang", "uz")
#             if lang not in REMINDER_MESSAGES:
#                 lang = "uz"

#             if minutes_left == 2:
#                 await bot.send_message(user_id, "keldi ishlashi kerak edi")  # to‘g‘ri format
#                 await bot.send_message(user_id, REMINDER_MESSAGES[lang]["rate"], reply_markup=get_feedback_keyboard())
#                 user["rate_sent"] = True
#                 updated = True
#             # ✅ 5 daqiqa qolganda
#             if minutes_left == 1:
#                 await bot.send_message(user_id, REMINDER_MESSAGES[lang]["5m"])
#                 asyncio.create_task(send_live_countdown(user_id, bot, WEBINAR_TIME, tz, minutes_left))

#             # ✅ 3 soat qolganda
#             if minutes_left == 180:
#                 await bot.send_message(user_id, REMINDER_MESSAGES[lang]["180m"])
#                 asyncio.create_task(send_live_countdown(user_id, bot, WEBINAR_TIME, tz, minutes_left))

#             # ✅ 12 soat qolganda
#             if minutes_left == 720:
#                 await bot.send_message(user_id, REMINDER_MESSAGES[lang]["12h"])

#             # ✅ 2 soat o‘tgach — bir marta yuboriladi



#         except Exception as e:
#             print(f"❌ Failed to send to {user_id}: {e}")
#             continue

#     # ✅ Faqat kerak bo‘lsa faylni saqlaymiz
#     if updated:
#         with open(WEBINAR_JSON, "w", encoding="utf-8") as f:
#             json.dump(users, f, indent=2, ensure_ascii=False)
REMINDER_MINUTES = [2, 5, 180, 720]

async def send_webinar_reminders(bot: Bot):
    print("🔄 Reminder function started...")

    if not Path(WEBINAR_FILE).exists():
        print("❌ Webinar file does not exist.")
        return

    with open(WEBINAR_FILE, "r", encoding="utf-8") as f:
        try:
            webinars = json.load(f)
            print(f"✅ Loaded webinar data: {len(webinars)} countries")
        except json.JSONDecodeError:
            print("❌ Invalid webinars.json format.")
            return

    now = datetime.now(tz)
    updated = False

    for country, webinar in webinars.items():
        time_str = webinar.get("datetime")
        if not time_str:
            print(f"⚠️ No datetime for {country}")
            continue

        try:
            webinar_time = datetime.fromisoformat(time_str)
        except Exception:
            print(f"❌ Invalid date format for {country}: {time_str}")
            continue

        minutes_left = int((webinar_time - now).total_seconds() / 60)
        print(f"⏱ {country.upper()} | {minutes_left} daqiqa qoldi")

        for user in webinar.get("users", []):
            user_id = user.get("id")
            lang = user.get("lang", "uz")

            if lang == "uzbek":
                lang = "uz"
            elif lang == "english":
                lang = "en"
            if lang not in REMINDER_MESSAGES:
                lang = "uz"

            if "sent" not in user:
                user["sent"] = []
            sent = user["sent"]
            
            for m in REMINDER_MINUTES:
                print(f"🔍 Tekshirilmoqda: {m} daqiqa eslatmasi")
                print(minutes_left, m)
                if m - 1 <= minutes_left <= m + 1 and m not in sent:
                    try:
                        print(f"📤 YUBORISH → {country.upper()} | User ID: {user_id} | {m} daqiqa qoldi")
                        text = REMINDER_MESSAGES[lang].get(f"{m}m", f"📌 {m} daqiqa qoldi!\nHavola: https://t.me/iapplyorg")
                        await bot.send_message(user_id, text)

                        if m == 5:
                            print("⏳ Live countdown boshlanmoqda...")
                            asyncio.create_task(send_live_countdown(user_id, bot, webinar_time, tz, minutes_left))

                        if m == 2:
                            print("📊 Fikr olish xabari yuborilmoqda...")
                            await bot.send_message(
                                user_id,
                                "📊 Webinar sizga yoqdimi? 1–5 gacha baho bering:",
                                reply_markup=get_feedback_keyboard()
                            )

                        user["sent"].append(m)
                        updated = True
                        print(f"✅ {m} daqiqa xabari yuborildi va `sent`ga qo‘shildi.")

                    except Exception as e:
                        print(f"❌ Failed to send to {user_id}: {e}")
                        continue

    if updated:
        with open(WEBINAR_FILE, "w", encoding="utf-8") as f:
            json.dump(webinars, f, indent=2, ensure_ascii=False)
        print("💾 Fayl yangilandi.")
    else:
        print("ℹ️ Hech qanday yangilanish bo‘lmadi.")

    print("✅ Reminder function finished.\n")



import asyncio
from datetime import datetime

def emoji_clock(time_str: str) -> str:
    mapping = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', ':': ':'
    }
    return ''.join(mapping.get(c, c) for c in time_str)

def format_time_left(minutes_left: int) -> str:
    if minutes_left < 60:
        return f"{minutes_left} daqiqa qoldi"
    else:
        hours = minutes_left // 60
        minutes = minutes_left % 60
        if minutes == 0:
            return f"{hours} soat qoldi"
        else:
            return f"{hours} soat {minutes} daqiqa qoldi"

async def send_live_countdown(chat_id, bot, WEBINAR_TIME, tz, minutes_left):
    time_text = format_time_left(minutes_left)
    # Asosiy eslatma xabari (o‘zgarmaydi)
    await bot.send_message(
        chat_id,
        f"""⏰ <b>Diqqat!</b> Webinargacha atigi <b>{time_text}</b> vaqt qoldi! 🎓

🗣 <b>Sizga tavsiya qilamiz:</b>
• Kompyuteringizni tayyorlang 💻
• Quloqchinlaringizni ulang 🎧
• Tinch joyda qulay joylashib oling 🪑
• Qahva yoki choy tayyorlab qo‘ying ☕️

📌 <b>Webinar davomida eslatmalar, havolalar va muhim ma’lumotlar beriladi.</b> Tayyor bo‘ling! 💡

⏳ <b>Jonli taymer quyida yangilanib boradi:</b>""",
        parse_mode="HTML"
    )

    # Taymer xabarini boshlaymiz
    msg_time = await bot.send_message(chat_id, "⏳ Taymer ishga tushdi...")

    while True:
        now = datetime.now(tz)
        diff = WEBINAR_TIME - now

        if diff.total_seconds() <= 0:
            await msg_time.edit_text("✅ Webinar boshlandi!", parse_mode="HTML")
            break

        hours, rem = divmod(int(diff.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        emoji_time = emoji_clock(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        try:
            await msg_time.edit_text(f"⏳ <b>Qolgan vaqt:</b> <code>{emoji_time}</code>", parse_mode="HTML")
        except Exception as e:
            print(f"[Edit error] {e}")

        await asyncio.sleep(2)  # Har 2 soniyada yangilanadi



def update_user_rating_in_webinar_file(user_id: int, rating: int):
    if not Path(WEBINAR_FILE).exists():
        print("⚠️ Webinar fayli mavjud emas")
        return

    with open(WEBINAR_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ JSON fayl formatida xatolik")
            return

    updated = False

    for country, webinar in data.items():
        for user in webinar.get("users", []):
            if user.get("id") == user_id:
                user["user_rate"] = rating
                updated = True
                print(f"✅ {user_id} foydalanuvchining bahosi {rating} ga o‘zgartirildi")
                break

    if updated:
        with open(WEBINAR_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print(f"⚠️ {user_id} user topilmadi.")


def update_user_feedback_in_webinar_file(user_id: int, feedback: str):
    if not Path(WEBINAR_FILE).exists():
        print("⚠️ Webinar fayli mavjud emas")
        return

    with open(WEBINAR_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ JSON fayl formatida xatolik")
            return

    updated = False

    for country, webinar in data.items():
        for user in webinar.get("users", []):
            if user.get("id") == user_id:
                user["user_feedback"] = feedback
                updated = True
                print(f"✅ {user_id} foydalanuvchining fikri saqlandi.")
                break

    if updated:
        with open(WEBINAR_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print(f"⚠️ {user_id} user topilmadi.")
