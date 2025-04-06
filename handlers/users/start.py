from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import aiogram.dispatcher.filters.state
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton
)
import os
from aiogram.dispatcher import FSMContext
from states.userState import Form, WebinarRegistration
from loader import dp, bot
from utils.lang import t, country_translations, translations
from icecream import ic
from datetime import datetime
import json
from utils.webinar_utils import save_user_to_webinar, get_webinar_countdown
# from data.config import GROUP_CHAT_ID, THREAD_ID
webinars = [
    {
        "id": "germany",
        "country": "Germaniya",
        "flag": "🇩🇪",
        "date": "10.04.2025",
        "time": "16:00",
        "mentor": "Ubaydullo Salohiddion"
    },
    {
        "id": "italy",
        "country": "Italiya",
        "flag": "🇮🇹",
        "date": "11.04.2025",
        "time": "12:00",
        "mentor": "Mirakbar Azimov"
    },
    # Boshqa vebinarlar ham shu yerga qo‘shiladi
]
# 🔒 Obuna tekshirish funksiyasi
async def check_subscription(user_id: int) -> bool:
    try:
        member_uz = await bot.get_chat_member(chat_id=-1002499834980, user_id=user_id)
        member_en = await bot.get_chat_member(chat_id=-1002144778879, user_id=user_id)
        return all([
            member_uz.status in ("member", "administrator", "creator"),
            member_en.status in ("member", "administrator", "creator")
        ])
    except:
        return False


# /start → webinar yoki contact flow
@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    args = message.get_args()
    ic(args)
    if args == "webinar":
        await state.update_data(entry_point="webinar")

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        )
        lang = message.from_user.language_code or "uz"
        await message.answer(t("choose_language", lang), reply_markup=keyboard)

    else:
        lang = "en"
        await state.update_data(lang=lang)
        await message.answer("👋 Welcome! Please enter your full name:")
        await Form.fullname.set()
def translate_country(country: str, lang: str) -> str:
    return country_translations.get(lang, {}).get(country, country)

def t(key: str, lang: str = "uz") -> str:
    return translations.get(lang, translations["uz"]).get(key, key)

@dp.message_handler(state=Form.webinar)
async def handler_webinar(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    language = state_data.get("lang", "uz")

    await message.answer(t("select_webinar", language))
    await message.answer(t("schedule_webinar", language))

    message_ids = []  # 🔥 Saqlab boramiz

    for index, webinar in enumerate(webinars, start=1):
        country = translate_country(webinar["country"], language)

        text = (
            f"🔍 {country} {t('webinar_intro', language)}\n"
            f"{index}\u20e3 {country} {t('webinar', language)} {webinar['flag']}\n"
            f"📅 {t('date', language)}: {webinar['date']}\n"
            f"🕒 {t('time', language)}: {webinar['time']}\n"
            f"🎙️ {t('mentor', language)}: {webinar['mentor']}\n"
        )

        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text=t("participate_webinar", language),
                callback_data=f"register:{webinar['id']}"
            )
        )

        msg = await message.answer(text, reply_markup=markup)
        message_ids.append(msg.message_id)  # 📌 Har bir yuborilgan xabar ID sini saqlaymiz

    final_msg = await message.answer(t("message_webinar", language))
    message_ids.append(final_msg.message_id)

    # 🔐 Xabar IDlarini state ichiga yozamiz
    await state.update_data(webinar_message_ids=message_ids)








# Til tanlandi → kanalga obuna qilish
@dp.callback_query_handler(lambda c: c.data.startswith("lang_"), state='*')
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[1]
    await state.update_data(lang=lang_code)
    await callback.message.delete()

    sub_buttons = InlineKeyboardMarkup(row_width=1)
    sub_buttons.add(
        InlineKeyboardButton("🇺🇿 iApply (UZ)", url="https://t.me/iapplyorguz"),
        InlineKeyboardButton("🇬🇧 iApply (EN)", url="https://t.me/iapplyorg"),
        InlineKeyboardButton(t("check_subscription", lang_code), callback_data="check_subs")
    )

    text = {
        "uz": "📢 Webinar’da ishtirok etishdan oldin quyidagi rasmiy kanallarga obuna bo‘ling:",
        "en": "📢 Please subscribe to the official channels before joining the webinar:"
    }

    await callback.message.answer(text.get(lang_code, text["uz"]), reply_markup=sub_buttons)
    # await Form.webinar.set()

# ✅ Obunani tekshirish tugmasi
@dp.callback_query_handler(lambda c: c.data == "check_subs", state='*')
async def check_subscriptions(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if not await check_subscription(user_id):
        msg = {
            "uz": "❌ Obuna aniqlanmadi. Iltimos, har ikkala kanallarga obuna bo‘ling.",
            "en": "❌ Subscription not found. Please subscribe to both channels."
        }
        await callback.answer(msg.get(lang, msg["uz"]), show_alert=True)
        return

    await callback.message.delete()

    # register_btn = InlineKeyboardMarkup().add(
    #     InlineKeyboardButton(t("register_button", lang), callback_data="start_register")
    # )

    # msg = {
    #     "uz": "✅ Obuna muvaffaqiyatli tasdiqlandi.",
    #     "en": "✅ Subscription confirmed."
    # }
    await Form.webinar.set()
    # await callback.message.answer(msg.get(lang, msg["uz"]), reply_markup=ReplyKeyboardRemove())
    await handler_webinar(callback.message, state)

@dp.callback_query_handler(lambda c: c.data.startswith("register:"), state=Form.webinar)
async def register_callback(callback: types.CallbackQuery, state: FSMContext):
    _, webinar_id = callback.data.split(":")
    webinar = next((w for w in webinars if w["id"] == webinar_id), None)

    data = await state.get_data()
    lang = data.get("lang") or callback.from_user.language_code[:2]
    if lang == 'ru':
        lang = 'en'
    elif lang not in ["uz", "en"]:
        lang = "uz"

    await state.update_data(lang=lang, selected_webinar=webinar)

    # 🔥 Oldingi webinar xabarlarini o‘chirish
    message_ids = data.get("webinar_message_ids", [])
    for msg_id in message_ids:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_id)
        except:
            pass  # Ba'zi xabarlar allaqachon o‘chirilgan bo‘lishi mumkin

    country = translate_country(webinar.get("country", "Unknown"), lang)

    await callback.message.answer(
        f"🎉 <b>{t('congrats_1_webinar', lang)} {country}</b> {t('congrats_2_webinar', lang)}\n\n"
        f"{t('ask_name', lang)}",
        parse_mode="HTML"
    )

    await WebinarRegistration.full_name.set()




@dp.message_handler(state=WebinarRegistration.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = data.get("lang", "uz")
    contact_button = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    ).add(
        KeyboardButton(t("share_phone", lang), request_contact=True)
    )

    await message.answer(
        t("send_phone", lang),
        reply_markup=contact_button,
        parse_mode="HTML"
    )
    await WebinarRegistration.phone.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=WebinarRegistration.phone)
async def get_phone_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    
    username = message.from_user.username
    full_username = f"@{username}" if username else "yo'q"
    await state.update_data(telegram_username=full_username)

    data = await state.get_data()
    data["user_id"] = message.from_user.id
    data["timestamp"] = datetime.now().isoformat()
    lang = data.get('lang')
    selected_webinar = data.get("selected_webinar")
    if selected_webinar:
        data["webinar_country"] = selected_webinar["country"]
        data["webinar_flag"] = selected_webinar["flag"]
        data["webinar_date"] = selected_webinar["date"]
        data["webinar_time"] = selected_webinar["time"]
        data["mentor"] = selected_webinar["mentor"]

    # ✅ Faylga array sifatida qo‘shib borish
    file_path = "users_database.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []  # ❗️ Fayl noto‘g‘ri formatda bo‘lsa tozalaymiz
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []


    existing_data.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    # ✅ Xabar
    await message.answer(
        t("congrats", lang),
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()





# 📥 Ro‘yxatdan o‘tish tugmasi bosilganda
@dp.callback_query_handler(lambda c: c.data == "start_register", state='*')
async def start_registration_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", callback.from_user.language_code or "uz")

    # 🎯 Faqat webinar bo‘lsa saqlaymiz
    if data.get("entry_point") == "webinar":
        user_data = {
            "id": callback.from_user.id,
            "fullname": None,
            "phone": None,
            "description": None,
            "lang": lang
        }
        print(user_data)
        save_user_to_webinar(user_data)

    await callback.message.delete()
    countdown_text = get_webinar_countdown()
    await callback.message.answer(countdown_text)
    # await callback.message.answer(t("thank_you", lang))
    await state.finish()



# 👤 Ism
@dp.message_handler(state=Form.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Please enter your full name.")
        return

    await state.update_data(fullname=message.text)
    await Form.phone.set()

    data = await state.get_data()
    lang = data.get("lang", message.from_user.language_code or "en")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton(t("send_phone", lang), request_contact=True)
    keyboard.add(button)

    await message.answer(t("send_phone", lang), reply_markup=keyboard)


# ☎️ Telefon
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await Form.description.set()

    data = await state.get_data()
    lang = data.get("lang", message.from_user.language_code or "en")

    await message.answer(t("description_prompt", lang), reply_markup=ReplyKeyboardRemove())


# 📝 Izoh
@dp.message_handler(state=Form.description)
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", message.from_user.language_code or "en")

    # entry_point = data.get("entry_point")
    # if entry_point == "webinar":
    #     user_data = {
    #         "id": message.from_user.id,
    #         "fullname": data.get("fullname"),
    #         "phone": data.get("phone"),
    #         "description": message.text,
    #         "lang": lang
    #     }
        # await message.answer(t("thank_you", lang))
    # await bot.send_message(
    #     GROUP_CHAT_ID,
    #     f"📋 New Form Submission:\n\n"
    #     f"👤 Full Name: {data.get('fullname')}\n"
    #     f"📞 Phone Number: {data.get('phone')}\n"
    #     f"📝 Description: {message.text}",
    #     message_thread_id=THREAD_ID
    # )
    await message.answer("✅ Thank you for the information! our iApply colleagues will contact you soon 😊")

    await state.finish()
