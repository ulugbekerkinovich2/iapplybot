from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import aiogram.dispatcher.filters.state
import aiogram.types
import aiogram.dispatcher
from aiogram.dispatcher import FSMContext
import re
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
import aiogram.utils.exceptions
import os
import aiogram.dispatcher
from aiogram.dispatcher.filters import Text
from states.userState import Form, WebinarRegistration
from loader import dp, bot
from utils.lang import t, country_translations, translations
from icecream import ic
from datetime import datetime
import json
from utils.webinar_utils import save_user_to_webinar
from aiogram.types import InputFile
from keyboards.inline.user_inlineKeyboards import inline_kb, country_kb, get_mentor_keyboard, language, application_buttons, sub_buttons, get_main_menu_keyboard,get_feedback_buttons,get_language_selection_keyboard,get_select_degree_inline,get_country_keyboard
from keyboards.default.user_menuButton import default_kb, request_phone, get_request_phone_keyboard
from data.config import GROUP_CHAT_ID, WEBINAR_THREAD_ID, WEBINAR_THREAD_ID_HELP
from utils.webinar_utils import WEBINAR_TIME, send_live_countdown
from states.userState import HelpForm

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

@dp.message_handler(commands=['change_language'], state="*")
async def change_language_(message: types.Message, state: FSMContext):
    print('change_language 40')
    await message.answer("Tilni tanlang:", reply_markup=language)
@dp.callback_query_handler(lambda c: c.data == "change_language", state='*')
async def change_language(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Tilni tanlang:", reply_markup=language)


@dp.message_handler(commands=['application'], state='*')
async def applcation_(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'en')
    print(lang, 46)
    if  lang == 'english' or lang == 'en':
        print(t('application_type', lang), 48)
        await message.answer(t('application_type', lang), reply_markup=get_feedback_buttons(lang))
    elif lang == 'uz' or lang == 'uzbek':
        print(t('application_type', lang), 51)
        await message.answer(t('application_type', lang), reply_markup=get_feedback_buttons(lang))

@dp.message_handler(commands=['vebinar'], state='*')
async def webinar_(message: types.Message, state: FSMContext):
    photo = InputFile("images/image2_1.jpg")
    data_ = await state.get_data()
    lang = data_.get('lang', 'uz')
    await message.answer_photo(
        photo=photo,
        caption=(t("webinar_main",lang )),
        # caption = "sd",
        parse_mode="HTML"
    )
    await message.answer(
        t('favourite_country', lang),
        reply_markup=country_kb
    )

@dp.message_handler(CommandStart(), state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)
    print(is_subscribed)
    if is_subscribed:
        full_text = "Assalomu Alaykum! iApply botiga xush kelibsiz 👋🏻\nDavom etish uchun tilni tanlang ⤵️"
        await message.answer(
            text=full_text,
            reply_markup=language,
            parse_mode="HTML"
        )
    else:
        if lang == "en":
            text = (
                "🚫 <b>Attention!</b> To use the bot, please subscribe to the following channels:\n\n"
                "📢 <a href='https://t.me/iapplyorg'>iApply (Uz)</a> — news and updates 🇺🇿\n"
                "🌍 <a href='https://t.me/iapplyorguz'>iApply (Eng)</a> — international webinars 🇬🇧\n\n"
                "✅ <b>After subscribing, click the button below.</b>"
            )
        else:
            text = (
                "🚫 <b>Diqqat!</b> Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:\n\n"
                "📢 <a href='https://t.me/iapplyorg'>iApply (Uz)</a> — yangiliklar, e’lonlar 🇺🇿\n"
                "🌍 <a href='https://t.me/iapplyorguz'>iApply (Eng)</a> — xalqaro vebinarlar 🇬🇧\n\n"
                "✅ <b>Obuna bo‘lganingizdan so‘ng pastdagi tugmani bosing.</b>"
            )

        await message.answer(
            text=text,
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton("📢 iApply (Uz)", url="https://t.me/iapplyorg"),
                types.InlineKeyboardButton("🌍 iApply (Eng)", url="https://t.me/iapplyorguz"),
                types.InlineKeyboardButton("✅ I have subscribed" if lang == "en" else "✅ Obuna bo‘ldim", callback_data="check_subscription")
            ),
            parse_mode="HTML",
            disable_web_page_preview=True
        )





@dp.callback_query_handler(lambda c: c.data in ['uzbek', 'english'], state='*')
async def fetch_language(callback: types.CallbackQuery, state: FSMContext):
    lang_ = callback.data
    await state.update_data(lang=lang_)

    if lang_ == 'english':
        msg = "Great! 👍 English selected 🇬🇧\nChoose one of the sections below to continue ⤵️"
    else:
        msg = "Ajoyib! 👍 O‘zbek tili tanlandi 🇺🇿\nKerakli bo‘limga o‘tish uchun tugmalardan birini tanlang ⤵️"

    await callback.message.answer(msg, reply_markup=get_main_menu_keyboard(lang_))



@dp.callback_query_handler(lambda d: d.data == "register_webinar", state='*')
async def start_register(callback: types.CallbackQuery, state: FSMContext):
    photo = InputFile("images/image2_1.jpg")
    data_ = await state.get_data()
    lang = data_.get('lang', 'uz')
    print(lang)
    if lang == "english" or lang == 'en':
        caption_text = t('webinar_main', 'en')
        # caption_text = "📢 Welcome to the iApply Webinar!\nFind opportunities to study abroad! 🌍"
        message_text = """💡Ready to Unlock Your Global Future?

Tap a country in which you are interested in studying below for tailored webinar details:🇹🇷|🇩🇪|🇰🇷|🇺🇸|🇮🇹|🇫🇮|🇳🇴|🇸🇪|🇨🇭|🇭🇺"""
    else:
        caption_text = t('webinar_main', 'uz')
        # caption_text = "📢 iApply vebinariga xush kelibsiz!\nChet elda o‘qish imkoniyatlarini bilib oling! 🌍"
        message_text = """💡 Butun dunyo eshiklarini ochishga tayyormisiz?

O‘qishni xohlayotgan mamlakatizni bayrog‘ini bosing va vebinar tafsilotlarini oling:🇹🇷|🇩🇪|🇰🇷|🇺🇸|🇮🇹|🇫🇮|🇳🇴|🇸🇪|🇨🇭|🇭🇺"""

    await callback.message.answer_photo(
        photo=photo,
        caption=caption_text,
        parse_mode="HTML"
    )

    await callback.message.answer(
        message_text,
        reply_markup=get_country_keyboard(lang)
    )


from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Tashkent")

webinar_times = {
    "turkey": tz.localize(datetime(2025, 4, 13, 21, 28)),
    "usa": tz.localize(datetime(2025, 4, 13, 21, 10)),
    "italy": tz.localize(datetime(2025, 4, 13, 21, 10)),
    "germany": tz.localize(datetime(2025, 4, 13, 21, 10)),
    "korea": tz.localize(datetime(2025, 4, 13, 21, 10)),
    "nordic": tz.localize(datetime(2025, 4, 13, 21, 10)),  
    "hungary": tz.localize(datetime(2025, 4, 13, 21, 10)),
}


@dp.callback_query_handler(lambda c: c.data in ['italy', 'turkey', 'usa', 'germany', 'korea', 'nordic', 'hungary'], state="*")
async def country_handler(callback: types.CallbackQuery, state: FSMContext):
    country = callback.data
    data = await state.get_data()
    lang = data.get('lang', 'uz')

    # Til formatlash
    if lang == 'english':
        lang = 'en'

    # ✅ Rasm va matn
    photo = InputFile(f"images/{country}.jpg")
    caption_text = t(country, lang)

    # ✅ Vaqtni aniqlash
    webinar_time = webinar_times.get(country)
    if webinar_time:
        await state.update_data(country=country, webinar_time=webinar_time.isoformat())
    else:
        print(f"⚠️ Vaqt yo'q: {country}")

    # ✅ Foydalanuvchiga yuborish
    await callback.message.answer_photo(
        photo=photo,
        caption=caption_text,
        reply_markup=get_mentor_keyboard(country, lang)
    )


@dp.callback_query_handler(lambda c: c.data.startswith("register_consultant"), state='*')
async def get_user_name(callback: types.CallbackQuery, state: FSMContext):
    # "register_consultant:turkey" → ["register_consultant", "turkey"]
    country = callback.data.split(":")[1]
    await state.update_data(country=country)

    data = await state.get_data()
    lang = data.get("lang", "uz")

    if lang == "english" or lang == 'en':
        text = "📝 Please enter your full name:"
    else:
        text = "📝 To‘liq ism familiyangizni kiriting:"

    await callback.message.answer(text)
    await Form.fullname.set()


@dp.message_handler(state=Form.fullname)
async def username_handler(message: types.Message, state: FSMContext):
    fullname_ = message.text
    await state.update_data(fullname=fullname_)

    data = await state.get_data()
    lang = data.get("lang", "uz")
    print(lang, 175)
    if lang == "en" or lang == "english":
        lang = 'en'
        text = "☎️ Please share your phone number."
    else:
        text = "☎️ Telefon raqamingizni yuboring."

    await message.answer(text, reply_markup=get_request_phone_keyboard(lang))
    await Form.phone.set()





PHONE_REGEX = re.compile(r"^\+998\d{9}$")  # +998 bilan boshlanuvchi format

@dp.message_handler(state=Form.phone, content_types=[ContentType.CONTACT, ContentType.TEXT])
async def phone_handler(message: Message, state: FSMContext):
    phone_ = None
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if message.contact:
        phone_ = message.contact.phone_number
    elif message.text and PHONE_REGEX.match(message.text):
        phone_ = message.text

    if phone_:
        await state.update_data(phone=phone_)

        # Matnlar lang bo‘yicha
        if lang == "en" or lang == 'english':
            accepted_msg = "✅ Your phone number has been accepted."
            degree_question = "🎓 Are you applying for a Bachelor's or Master's degree?"
        else:
            accepted_msg = "✅ Telefon raqamingiz qabul qilindi."
            degree_question = "🎓 Siz chet el universitetlarida bakalavrda o'qimoqchimisiz yoki magistrda?"

        await message.answer(accepted_msg, reply_markup=ReplyKeyboardRemove())
        await Form.ask_degree.set()
        await message.answer(degree_question, reply_markup=get_select_degree_inline(lang))

    else:
        if lang == "en":
            error_text = (
                "❌ Please enter a valid phone number or share your contact.\nExample: +998901234567"
            )
        else:
            error_text = (
                "❌ Iltimos, haqiqiy telefon raqamingizni yozing yoki kontakt yuboring.\nMasalan: +998901234567"
            )
        await message.answer(error_text)









@dp.callback_query_handler(lambda c: c.data in ['master', 'bachelor'], state="*")
async def degree_handler(callback: types.CallbackQuery, state: FSMContext):
    degree_level = callback.data
    await state.update_data(degree=degree_level)

    data = await state.get_data()
    rate_ = data.get("rate")
    lang = data.get("lang", "uz")
    if lang == "english":
        lang = "en"

    await callback.answer()  # ✅ Loading tugmasini yopish

    # ✅ Userga habar yuborish
    if lang == "en":
        message_text = (
            "✅ Thank you! You’ve *successfully* registered.\n"
            "📌 We’ll keep you updated with important notifications."
        )
    else:
        message_text = (
            "✅ Rahmat! Siz *muvaffaqiyatli* ro'yhatdan o'tdingiz.\n"
            "📌 Biz sizga muhim eslatmalarni hali yuborib turamiz."
        )

    await callback.message.answer(message_text, parse_mode="Markdown")

    # ✅ Admin kanalga habar
    await bot.send_message(
        GROUP_CHAT_ID,
        f"📋 New Form Submission:\n\n"
        f"👤 Full Name: {data.get('fullname')}\n"
        f"📞 Phone Number: {data.get('phone')}\n"
        f"📝 Degree: {degree_level}",
        message_thread_id=WEBINAR_THREAD_ID
    )

    # ✅ Vebinar vaqti va mamlakatni olish
    country = data.get("country")
    webinar_time = data.get("webinar_time")

    # ✅ Yangi user ma'lumotlari
    user_data = {
        "id": callback.from_user.id,
        "fullname": data.get('fullname'),
        "phone": data.get("phone"),
        "degree": degree_level,
        "lang": lang,
        "country": country,
        "webinar_time": webinar_time,  # 🆕 Qo‘shilgan qism,
        "user_rate": rate_,
        "user_feedback": data.get("support")
    }

    print(user_data)
    save_user_to_webinar(user_data)

    await state.finish()





    # await send_live_countdown(callback.message.chat.id, bot)

    # now = datetime.utcnow()
    # WEBINAR_TIME = datetime(2025, 4, 10, 18, 0, 0)
    # diff = WEBINAR_TIME - now

    # if diff.total_seconds() <= 0:
    #     await callback.message.answer("✅ Webinar allaqachon boshlangan yoki tugagan.")
    # else:
    #     hours, rem = divmod(int(diff.total_seconds()), 3600)
    #     minutes, seconds = divmod(rem, 60)
    #     await callback.message.answer(
    #         f"⏳ Webinargacha qolgan vaqt: {hours} soat {minutes} daqiqa {seconds} soniya"
    #     )

@dp.callback_query_handler(lambda c: c.data == "cancel", state="*")
async def cancel_handler_callback(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data, 1)
    full_text = """Assalomu Alaykum! iApply botiga xush kelibsiz 👋🏻Davom etish uchun tilni tanlang ⤵️"""
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    # 1. Rasm va qisqa caption bilan
    await callback.message.answer(
        # photo=photo,
        text=full_text,
        reply_markup=get_language_selection_keyboard(lang),
        parse_mode="HTML"
    )
    await state.finish()



@dp.callback_query_handler(lambda c: c.data.startswith("rate_"), state='*')
async def handle_rating(callback: types.CallbackQuery, state: FSMContext):
    from utils.webinar_utils import update_user_rating_in_webinar_file
    rating = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    await state.update_data(rate=rating, user_id=user_id)
    data = await state.get_data()
    lang = data.get("lang", "uz")
    print(f"🎯 {user_id} dan {rating} baho olindi")

    # 🛠 JSON faylni yangilash
    update_user_rating_in_webinar_file(user_id, rating)

    if lang == "en" or lang == 'english':
        response = "✅ Thank you for your rating!"
        mes = "Thank you! Now share your thoughts about the webinar!"
    else:
        response = "✅ Bahoyingiz uchun rahmat!"
        mes = "Rahmat! Endi webinar haqida fikringiz bilan ulashing!"

    await callback.answer(response)
    await callback.message.answer(mes)
    await Form.support_webinar.set()


@dp.message_handler(state=Form.support_webinar)
async def process_support_webinar(message: types.Message, state: FSMContext):
    from utils.webinar_utils import update_user_feedback_in_webinar_file
    await state.update_data(support=message.text)
    data = await state.get_data()
    lang = data.get("lang", "uz")
    user_id = data.get("user_id") or message.from_user.id
    print(f"📝 {user_id} dan feedback olindi: {message.text}")

    # 🛠 JSON faylga yozamiz
    update_user_feedback_in_webinar_file(user_id, message.text)

    if lang == "en" or lang == 'english':
        await message.answer("✅ Thank you for your feedback! Our team will get back to you soon.")
    else:
        await message.answer("✅ Fikringiz uchun rahmat! Tez orada siz bilan bog‘lanamiz.")
    await state.finish()



@dp.callback_query_handler(lambda c: c.data == 'help', state='*')
async def handler_help(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    print(lang, 354)
    if lang == "en" or lang == 'english':
        # await callback.message.answer("Sizni arizangiz qanaqa ko'rinishda?", reply_markup=application_buttons)
        await callback.message.answer("What kind of application do you have?", reply_markup=get_feedback_buttons(lang))
    else:
        await callback.message.answer("Sizni arizangiz qanaqa ko'rinishda?", reply_markup=get_feedback_buttons(lang))

@dp.callback_query_handler(lambda text: text.data in ['taklif', 'shikoyat', 'konsultatsiya'])
async def fetch_help(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data
    await state.update_data(type_application=data)

    user_data = await state.get_data()
    lang = user_data.get("lang", "uz")
    print(lang)
    if lang == "english" or lang == "en":
        msg = "Please enter your full name:"
    else:
        msg = "To‘liq ism familiyangizni kiriting:"

    await callback.message.answer(msg)
    await HelpForm.fullname.set()



@dp.message_handler(state=HelpForm.fullname)
async def fetch_phone(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(fullname=full_name)

    data = await state.get_data()
    lang = data.get("lang", "uz")

    if lang == "english":
        text = "☎️ Please send your phone number."
    else:
        text = "☎️ Telefon raqamingizni yuboring."

    await message.answer(text, reply_markup=request_phone)
    await HelpForm.phone.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=HelpForm.phone)
async def fetch_application(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone=phone_number)

    data = await state.get_data()
    lang = data.get("lang", "uz")

    if lang == "english":
        text = "📝 Now please write and send your message."
    else:
        text = "📝 Endi iltimos, murojaatingizni yozib yuboring."

    await message.answer(text)


    await HelpForm.application_type.set()  # yoki: await HelpForm.application_text.set()
@dp.message_handler(state=HelpForm.application_type)
async def finish_(message: types.Message, state: FSMContext):
    user_text = message.text
    data = await state.get_data()
    lang = data.get("lang", "uz")

    # Guruhga yuboriladigan matn — bu doim inglizcha yoki administratorga mos bo‘lishi mumkin,
    # lekin kerak bo‘lsa, type_application qiymatini ham tarjima qilish mumkin:
    type_application_map = {
        "uz": {
            "taklif": "Taklif",
            "shikoyat": "Shikoyat",
            "konsultatsiya": "Konsultatsiya"
        },
        "en": {
            "taklif": "Suggestion",
            "shikoyat": "Complaint",
            "konsultatsiya": "Consultation"
        }
    }

    type_label = type_application_map.get(lang, type_application_map["uz"]).get(data.get('type_application'), data.get('type_application'))

    await bot.send_message(
        GROUP_CHAT_ID,
        f"📋 New Form Submission:\n\n"
        f"👤 Full Name: {data.get('fullname')}\n"
        f"📞 Phone Number: {data.get('phone')}\n"
        f"📝 #{type_label}: {user_text}",
        message_thread_id=WEBINAR_THREAD_ID_HELP,
        parse_mode="Markdown"
    )

    # Foydalanuvchiga chiqadigan javob
    if lang == "english":
        response = "✅ Thank you! We will contact you very soon!"
    else:
        response = "✅ Rahmat! Siz bilan tez orada aloqaga chiqamiz!"

    await message.answer(response)
    await state.finish()


# async def send_cancel_info(target):
#     photo = InputFile("images/iapply_image.jpg")
#     full_text = """
#     <b>📌 What does the scholarship cover?</b>

#     <b>📞 Contact Information:</b>  
#     📲 <b>Phone:</b> +998 78 113 14 80
#     ✉️ <b>Email:</b> <a href="mailto:info@iapply.org">info@iapply.org</a>  
#     💬 <b>Telegram:</b> <a href="https://t.me/iapplyhelp">@iapplyhelp</a>

#     <b>🌐 More Links:</b>  
#     🌎 <a href="https://iapply.org/">Website</a> | 🕊 <a href="https://t.me/iapplyorg">Telegram</a> | 📱 <a href="https://www.instagram.com/iapply_org?igsh=MWhjdWJra2YwMjdqNQ==">Instagram</a>
#     """
#     await target.answer_photo(
#         photo=photo,
#         caption=full_text,
#         parse_mode="HTML"
#     )

    # get_webinar_countdown()
    # await target.answer(
    #     full_text,
    #     reply_markup=inline_kb,
    #     parse_mode="HTML"
    # )





# def translate_country(country: str, lang: str) -> str:
#     return country_translations.get(lang, {}).get(country, country)

# def t(key: str, lang: str = "uz") -> str:
#     return translations.get(lang, translations["uz"]).get(key, key)

# @dp.message_handler(state=Form.webinar)
# async def handler_webinar(message: types.Message, state: FSMContext):
#     state_data = await state.get_data()
#     language = state_data.get("lang", "uz")

#     await message.answer(t("select_webinar", language))
#     await message.answer(t("schedule_webinar", language))

#     message_ids = []  # 🔥 Saqlab boramiz

#     for index, webinar in enumerate(webinars, start=1):
#         country = translate_country(webinar["country"], language)

#         text = (
#             f"🔍 {country} {t('webinar_intro', language)}\n"
#             f"{index}\u20e3 {country} {t('webinar', language)} {webinar['flag']}\n"
#             f"📅 {t('date', language)}: {webinar['date']}\n"
#             f"🕒 {t('time', language)}: {webinar['time']}\n"
#             f"🎙️ {t('mentor', language)}: {webinar['mentor']}\n"
#         )

#         markup = InlineKeyboardMarkup().add(
#             InlineKeyboardButton(
#                 text=t("participate_webinar", language),
#                 callback_data=f"register:{webinar['id']}"
#             )
#         )

#         msg = await message.answer(text, reply_markup=markup)
#         message_ids.append(msg.message_id)  # 📌 Har bir yuborilgan xabar ID sini saqlaymiz

#     final_msg = await message.answer(t("message_webinar", language))
#     message_ids.append(final_msg.message_id)

#     # 🔐 Xabar IDlarini state ichiga yozamiz
#     await state.update_data(webinar_message_ids=message_ids)


# # Til tanlandi → kanalga obuna qilish
@dp.callback_query_handler(lambda c: c.data.startswith("lang_"), state='*')
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[1]
    await state.update_data(lang=lang_code)
    await callback.message.delete()

    await callback.message.answer(t("subscribe", lang_code), reply_markup=sub_buttons)
    await Form.webinar.set()

# # ✅ Obunani tekshirish tugmasi
@dp.callback_query_handler(lambda c: c.data == "check_subscription", state='*')
async def check_subscriptions(callback: types.CallbackQuery, state: FSMContext):
    from keyboards.inline.user_inlineKeyboards import check_subscription_keyboard
    user_id = callback.from_user.id
    data = await state.get_data()
    lang = data.get("lang", "uz")

    # 🔎 A'zolikni tekshiramiz
    is_subscribed = await check_subscription(user_id)

    if not is_subscribed:
        # ❌ Aʼzo bo‘lmagan foydalanuvchiga xabar yuboramiz
        await callback.message.answer(
            t("err_subscription", lang),  # Masalan: "📢 Avval kanallarga a’zo bo‘ling!"
            reply_markup=check_subscription_keyboard(lang)  # ➕ Aʼzo bo‘lish tugmalari
        )
        return

    # ✅ Aʼzo bo‘lgan — davom etamiz
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"⚠️ delete() xatolik: {e}")

    await Form.webinar.set()
    await callback.message.answer(
        t("success_subscription", lang),  # Masalan: "✅ A’zo bo‘lganingiz tasdiqlandi!"
        reply_markup=language
    )


    # await handler_webinar(callback.message, state)

# @dp.callback_query_handler(lambda c: c.data.startswith("register:"), state=Form.webinar)
# async def register_callback(callback: types.CallbackQuery, state: FSMContext):
#     _, webinar_id = callback.data.split(":")
#     webinar = next((w for w in webinars if w["id"] == webinar_id), None)

#     data = await state.get_data()
#     lang = data.get("lang") or callback.from_user.language_code[:2]
#     if lang == 'ru':
#         lang = 'en'
#     elif lang not in ["uz", "en"]:
#         lang = "uz"

#     await state.update_data(lang=lang, selected_webinar=webinar)

#     # 🔥 Oldingi webinar xabarlarini o‘chirish
#     message_ids = data.get("webinar_message_ids", [])
#     for msg_id in message_ids:
#         try:
#             await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_id)
#         except:
#             pass  # Ba'zi xabarlar allaqachon o‘chirilgan bo‘lishi mumkin

#     country = translate_country(webinar.get("country", "Unknown"), lang)

#     await callback.message.answer(
#         f"🎉 <b>{t('congrats_1_webinar', lang)} {country}</b> {t('congrats_2_webinar', lang)}\n\n"
#         f"{t('ask_name', lang)}",
#         parse_mode="HTML"
#     )

#     await WebinarRegistration.full_name.set()




# @dp.message_handler(state=WebinarRegistration.full_name)
# async def get_full_name(message: types.Message, state: FSMContext):
#     await state.update_data(full_name=message.text)
#     data = await state.get_data()
#     lang = data.get("lang", "uz")
#     contact_button = ReplyKeyboardMarkup(
#         resize_keyboard=True,
#         one_time_keyboard=True
#     ).add(
#         KeyboardButton(t("share_phone", lang), request_contact=True)
#     )

#     await message.answer(
#         t("send_phone", lang),
#         reply_markup=contact_button,
#         parse_mode="HTML"
#     )
#     await WebinarRegistration.phone.set()


# @dp.message_handler(content_types=types.ContentType.CONTACT, state=WebinarRegistration.phone)
# async def get_phone_contact(message: types.Message, state: FSMContext):
#     await state.update_data(phone=message.contact.phone_number)
    
#     username = message.from_user.username
#     full_username = f"@{username}" if username else "yo'q"
#     await state.update_data(telegram_username=full_username)

#     data = await state.get_data()
#     data["user_id"] = message.from_user.id
#     data["timestamp"] = datetime.now().isoformat()
#     lang = data.get('lang')
#     selected_webinar = data.get("selected_webinar")
#     if selected_webinar:
#         data["webinar_country"] = selected_webinar["country"]
#         data["webinar_flag"] = selected_webinar["flag"]
#         data["webinar_date"] = selected_webinar["date"]
#         data["webinar_time"] = selected_webinar["time"]
#         data["mentor"] = selected_webinar["mentor"]

#     # ✅ Faylga array sifatida qo‘shib borish
#     file_path = "users_database.json"
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             try:
#                 existing_data = json.load(f)
#                 if not isinstance(existing_data, list):
#                     existing_data = []  # ❗️ Fayl noto‘g‘ri formatda bo‘lsa tozalaymiz
#             except json.JSONDecodeError:
#                 existing_data = []
#     else:
#         existing_data = []


#     existing_data.append(data)

#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(existing_data, f, ensure_ascii=False, indent=2)

#     # ✅ Xabar
#     await message.answer(
#         t("congrats", lang),
#         parse_mode="HTML",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await state.finish()



# # 📥 Ro‘yxatdan o‘tish tugmasi bosilganda
# @dp.callback_query_handler(lambda c: c.data == "start_register", state='*')
# async def start_registration_callback(callback: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     lang = data.get("lang", callback.from_user.language_code or "uz")

#     # 🎯 Faqat webinar bo‘lsa saqlaymiz
#     if data.get("entry_point") == "webinar":
#         user_data = {
#             "id": callback.from_user.id,
#             "fullname": None,
#             "phone": None,
#             "description": None,
#             "lang": lang
#         }
#         print(user_data)
#         save_user_to_webinar(user_data)

#     await callback.message.delete()
#     countdown_text = get_webinar_countdown()
#     await callback.message.answer(countdown_text)
#     # await callback.message.answer(t("thank_you", lang))
#     await state.finish()



# # 👤 Ism
# @dp.message_handler(state=Form.fullname)
# async def process_fullname(message: types.Message, state: FSMContext):
#     if not message.text:
#         await message.answer("Please enter your full name.")
#         return

#     await state.update_data(fullname=message.text)
#     await Form.phone.set()

#     data = await state.get_data()
#     lang = data.get("lang", message.from_user.language_code or "en")

#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button = KeyboardButton(t("send_phone", lang), request_contact=True)
#     keyboard.add(button)

#     await message.answer(t("send_phone", lang), reply_markup=keyboard)


# # ☎️ Telefon
# @dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
# async def process_contact(message: types.Message, state: FSMContext):
#     await state.update_data(phone=message.contact.phone_number)
#     await Form.description.set()

#     data = await state.get_data()
#     lang = data.get("lang", message.from_user.language_code or "en")

#     await message.answer(t("description_prompt", lang), reply_markup=ReplyKeyboardRemove())


# # 📝 Izoh
# @dp.message_handler(state=Form.description)
# async def process_description(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     lang = data.get("lang", message.from_user.language_code or "en")

#     entry_point = data.get("entry_point")
#     if entry_point == "webinar":
#         user_data = {
#             "id": message.from_user.id,
#             "fullname": data.get("fullname"),
#             "phone": data.get("phone"),
#             "description": message.text,
#             "lang": lang
#         }
#         await message.answer(t("thank_you", lang))
#     await bot.send_message(
#         GROUP_CHAT_ID,
#         f"📋 New Form Submission:\n\n"
#         f"👤 Full Name: {data.get('fullname')}\n"
#         f"📞 Phone Number: {data.get('phone')}\n"
#         f"📝 Description: {message.text}",
#         message_thread_id=THREAD_ID
#     )
#     await message.answer("✅ Thank you for the information! our iApply colleagues will contact you soon 😊")

    # await state.finish()
