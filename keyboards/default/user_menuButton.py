from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False
)

default_kb.row(
    KeyboardButton("❌ Bekor qilish"),  # ❌ yoki 🔙 yoki ⛔ — bekor qilish uchun mos
    KeyboardButton("🔙 Ortga")          # 🔙 yoki ↩️ — orqaga qaytish uchun mos
)


request_phone_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True  # faqat bitta marta ko‘rinadi
)
request_phone_uz.add(
    KeyboardButton(text="☎️ Telefon raqamni yuborish", request_contact=True)
)

request_phone_en = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True  # faqat bitta marta ko‘rinadi
)
request_phone_en.add(
    KeyboardButton(text="☎️ Share your phone number", request_contact=True)
)


def get_request_phone_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    if lang == "en":
        btn_text = "☎️ Send phone number"
    else:
        btn_text = "☎️ Telefon raqamni yuborish"

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text=btn_text, request_contact=True))
    return keyboard
