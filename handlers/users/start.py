from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import aiogram.dispatcher.filters.state
import aiogram.types
import aiogram.dispatcher
from aiogram.dispatcher import FSMContext
import data
import re
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
import aiogram.utils.exceptions
import os
import aiofiles
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
from keyboards.inline.user_inlineKeyboards import inline_kb,country_kb_en, country_kb_uz, get_mentor_keyboard, language, application_buttons, sub_buttons, get_main_menu_keyboard,get_feedback_buttons,get_language_selection_keyboard,get_select_degree_inline,get_country_keyboard
from keyboards.default.user_menuButton import default_kb, request_phone_en, request_phone_uz, get_request_phone_keyboard
from data.config import GROUP_CHAT_ID,TEST_GROUP_CHAT_ID, WEBINAR_THREAD_FEEDBACK,TEST_WEBINAR_THREAD_FEEDBACK, WEBINAR_THREAD_ID_HELP,TEST_WEBINAR_THREAD_ID_HELP, WEBINAR_REGISTER_ID,TEST_WEBINAR_REGISTER_ID, ADMINS
from utils.webinar_utils import send_live_countdown
from states.userState import HelpForm
from utils.webinar_exporter import send_webinar_excel
from keyboards.inline.user_inlineKeyboards import get_language_keyboard

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

@dp.message_handler(commands=['changelanguage'], state="*")
async def change_language_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", None)
    print(lang)
    msg = "Tilni tanlang:" if lang == "uz" or lang=='uzbek' else "Please choose a language:"
    await message.answer(msg, reply_markup=get_language_keyboard())


@dp.callback_query_handler(lambda c: c.data == "change_language", state="*")
async def change_language_callback(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", None)
    msg = "Tilni tanlang:" if lang == "uz" or lang=='uzbek' else "Please choose a language:"
    await call.message.answer(msg, reply_markup=get_language_keyboard())
    await call.answer()



@dp.message_handler(commands=['help'], state='*')
async def applcation_(message: types.Message, state: FSMContext):
    await state.update_data(last_command='help')
    data = await state.get_data()
    lang = data.get('lang', 'en')
    print(lang, 46)

    caption = (
        "What kind of application do you have?"
        if lang in ("en", "english")
        else "Sizning arizangiz qanaqa ko'rinishda?"
    )

    # 🔍 Avval keshdan file_id izlaymiz
    file_id_data = load_file_id()
    if file_id := file_id_data.get("image_help"):
        await message.answer_photo(
            photo=file_id,
            caption=caption,
            reply_markup=get_feedback_buttons(lang)
        )
        return

    # 🌐 URL'dan rasm yuklab olish (birinchi marta)
    image_url = "https://demoapi.iapply.org/uni_gallery/78f6836b-480a-4553-a9e4-f16f6750a3d2.png"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(await resp.read())
                        tmp_path = tmp_file.name

                    input_photo = InputFile(tmp_path)
                    msg = await message.answer_photo(
                        photo=input_photo,
                        caption=caption,
                        reply_markup=get_feedback_buttons(lang)
                    )

                    # 🧠 file_id ni saqlaymiz
                    file_id = msg.photo[-1].file_id
                    save_file_id(file_id)
                else:
                    await message.answer("❌ Rasmni yuklab bo‘lmadi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")


@dp.message_handler(commands=['webinar'], state='*')
async def webinar_(message: types.Message, state: FSMContext):
    photo = InputFile("images/image2_1.jpg")
    data_ = await state.get_data()
    lang = data_.get('lang', None)
    if lang == 'english' or lang == 'en':
        lang = 'en'
        country_kb = country_kb_en
    if lang == 'uzbek' or lang == 'uz':
        lang = 'uz'
        country_kb = country_kb_uz
    print(lang)
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
    lang = data.get('lang', 'uz')  # default to 'uz'
    user_id = message.from_user.id

    is_subscribed = await check_subscription(user_id)
    print(f"✅ SUBSCRIBED: {is_subscribed}")

    if is_subscribed:
        text = (
            "Assalomu Alaykum! iApply botiga xush kelibsiz 👋🏻\nDavom etish uchun tilni tanlang ⤵️"
            if lang == "uz" or lang == "uzbek" else
            "Hello! Welcome to the iApply bot 👋🏻\nPlease select a language to continue ⤵️"
        )

        await message.answer(
            text=text,
            reply_markup=language,  # sizning til tanlash inline keyboard'ingiz
            parse_mode="HTML"
        )
    if not is_subscribed:
        # await message.answer("📛 Obuna bo‘lmagansiz. Iltimos, avval kanalga obuna bo‘ling.")


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
        msg = "Great! 👍 English selected 🇺🇸\nChoose one of the sections below to continue ⤵️"
    else:
        msg = "Ajoyib! 👍 O‘zbek tili tanlandi 🇺🇿\nKerakli bo‘limga o‘tish uchun tugmalardan birini tanlang ⤵️"

    await callback.message.answer(msg, reply_markup=get_main_menu_keyboard(lang_))

def check_user_exists(user_id, country__):
    file_path = os.path.join(os.path.dirname(__file__), '../../data/webinar_users.json')

    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    country_data = data.get(country__)
    if not country_data:
        return False

    users = country_data.get("users", [])
    for user in users:
        if user.get("id") == user_id:
            return True

    return False


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
    "turkey": tz.localize(datetime(2025, 4, 23, 23, 16)),
    "usa": tz.localize(datetime(2025, 4, 21, 18, 18)),
    "italy": tz.localize(datetime(2025, 4, 23, 13, 16)),
    "germany": tz.localize(datetime(2025, 4, 21, 18, 18)),
    "korea": tz.localize(datetime(2025, 4, 21, 18, 18)),
    "nordic": tz.localize(datetime(2025, 4, 23, 13, 31)),  
    "hungary": tz.localize(datetime(2025, 4, 21, 18, 18)),
}


@dp.callback_query_handler(lambda c: c.data in ['italy', 'turkey', 'usa', 'germany', 'korea', 'nordic', 'hungary'], state="*")
async def country_handler(callback: types.CallbackQuery, state: FSMContext):
    country = callback.data
    await state.update_data(country=country)
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
    # await callback.message.edit_reply_markup(reply_markup=None)
    country_map = {
        "turkey": {"uz": "🇹🇷 Turkiya", "en": "🇹🇷 Turkey"},
        "germany": {"uz": "🇩🇪 Germaniya", "en": "🇩🇪 Germany"},
        "usa": {"uz": "🇺🇸 AQSH", "en": "🇺🇸 USA"},
        "italy": {"uz": "🇮🇹 Italiya", "en": "🇮🇹 Italy"},
        "korea": {"uz": "🇰🇷 Janubiy Koreya", "en": "🇰🇷 South Korea"},
        "hungary": {"uz": "🇭🇺 Vengriya", "en": "🇭🇺 Hungary"},
        "nordic": {"uz": "🇫🇮 / 🇳🇴 / 🇸🇪 / 🇨🇭 Nordic Davlatlari", "en": "🇫🇮 / 🇳🇴 / 🇸🇪 / 🇨🇭 Nordic Countries"}
    }

    # "register_consultant:turkey" → ["register_consultant", "turkey"]
    country = callback.data.split(":")[1]
    await state.update_data(country=country)
    get_country = country_map.get(country)
    print('✅ callback keldi: register_webinar')
    check_user = check_user_exists(callback.from_user.id, country)
    if check_user:
        data = await state.get_data()
        lang = data.get('lang', None)
        if lang == "english" or lang == 'en':
            lang_ = 'en'
            await callback.message.answer(f"You have already registered for the webinar for {get_country[lang_]}! We encourage you to register for other webinars!")
        else:
            lang_ = 'uz'
            await callback.message.answer(f"Siz {get_country[lang_]} uchun webinar da ro'yhatdan o'tib bo'lgansiz! Sizga boshqa webinarlarda ishtirok etish uchun ro'yhatdan o'tishni tavsiya etamiz!")
    if not check_user:
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
    country_ = data.get("country")
    rate_ = data.get("rate")
    lang = data.get("lang", "uz")
    if lang == "english":
        lang = "en"

    await callback.answer()  # ✅ Loading tugmasini yopish
    users_by_country = {
        "italy": "Abdurakhmon Jumanazarov & Shohjahon Jonmirzayev",
        "usa": "Mahliyo Shavkatova",
        "turkey": "Gulbanu Turganbaeva",
        "nordic": "Shohjahon Jonmirzayev",
        "hungary": "Sarvinoz Yusupova",
        "germany": "Adhambek Yashnarbekov",
        "korea": "Begoyim Bekmirzaeva"
    }
    time_by_country = {
        "italy": "18.04.2025,20:00",
        "usa": "18.04.2025,20:00",
        "turkey": "18.04.2025,20:00",
        "nordic": "18.04.2025,20:00",
        "hungary": "18.04.2025,20:00",
        "germany": "18.04.2025,20:00",
        "korea": "18.04.2025,20:00"
    }
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
    country_map = {
        "turkey": "🇹🇷",
        "germany": "🇩🇪",
        "italy": "🇮🇹",
        "hungary": "🇭🇺",
        "korea": "🇰🇷",
        "nordic": "🇳🇴/🇸🇪/🇫🇮/🇨🇭",
        "usa": "🇺🇸"
    }
    country_names = {
        'turkey': "Turkey",
        'germany': "Germany",
        'italy': "Italy",
        'hungary': "Hungary",
        'korea': "South Korea",
        'nordic': "Nordic Countries",
        'usa': "USA"
    }
    if callback.from_user.username is not None:
        username_ = f"@{callback.from_user.username}"
    else:
        username_ = None
    # ✅ Admin kanalga habar
    await bot.send_message(
        GROUP_CHAT_ID,
        f"Country: {country_names.get(country_)} {country_map.get(country_)}\n"
        f"Mentor: {users_by_country.get(country_)}\n"
        f"Webinar date: {time_by_country.get(country_).split(',')[0]}\n"
        f"Webinar time: {time_by_country.get(country_).split(',')[1]}\n"
        f"Full name: {data.get('fullname')}\n"
        f"Phone number: {data.get('phone')}\n"
        f"Degree: {degree_level.capitalize()}\n"
        f"Telegram username: {username_}\n",
        message_thread_id=WEBINAR_REGISTER_ID
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
        "user_feedback": data.get("support"),
        "username": callback.from_user.username
    }

    print(user_data)
    save_user_to_webinar(user_data)
    await state.finish()



@dp.callback_query_handler(lambda c: c.data == "cancel", state="*")
async def cancel_handler_callback(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data, 1)
    full_text = """Assalomu Alaykum! iApply botiga xush kelibsiz 👋🏻\nDavom etish uchun tilni tanlang ⤵️"""
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


import json
from pathlib import Path

WEBINAR_JSON = Path("data/webinar_users.json")

def load_user_from_webinar_file(user_id: int):
    if not WEBINAR_JSON.exists():
        return None

    with open(WEBINAR_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for country_data in data.values():
        for user in country_data.get("users", []):
            if user.get("id") == user_id:
                return user
    return None


@dp.message_handler(state=Form.support_webinar)
async def process_support_webinar(message: types.Message, state: FSMContext):
    from utils.webinar_utils import update_user_feedback_in_webinar_file

    user_id = message.from_user.id
    feedback_text = message.text.strip()

    user_data = load_user_from_webinar_file(user_id)
    if not user_data:
        await message.answer("❌ Maʼlumot topilmadi.")
        await state.finish()
        return

    country = user_data.get("country", "").lower().strip()
    lang = user_data.get("lang", "uz")
    rate = user_data.get("user_rate", "N/A")

    mentors_by_country = {
        "italy": [
            ("Abdurakhmon Jumanazarov", "https://iapply.org/mentor/profile/abdurakhmon-jumanazarov-18?application="),
            ("Shohjahon Jonmirzayev", "https://iapply.org/mentor/profile/shohjahon-jonmirzayev-19?application=")
        ],
        "usa": [("Mahliyo Shavkatova", "https://iapply.org/mentor/profile/mahliyo-shavkatova-17?application=")],
        "turkey": [("Gulbanu Turganbaeva", "https://iapply.org/mentor/profile/gulbanu-turganbaeva-21?application=")],
        "nordic": [("Shohjahon Jonmirzayev", "https://iapply.org/mentor/profile/shohjahon-jonmirzayev-19?application=")],
        "hungary": [("Sarvinoz Yusupova", "https://iapply.org/mentor/profile/sarvinoz-yusupova-25?application=")],
        "germany": [("Adhambek Yashnarbekov", "https://iapply.org/mentor/profile/adhambek-yashnarbekov-20?application=")],
        "korea": [("Begoyim Bekmirzaeva", "https://iapply.org/mentor/profile/begoyim-bekmirzaeva-22?application=")]
    }

    mentors = mentors_by_country.get(country, [])

    dt = datetime.fromisoformat(user_data.get("webinar_time"))
    webinar_date = dt.strftime("%d.%m.%Y")
    webinar_time = dt.strftime("%H:%M")

    # 📤 Admin/gruppaga xabar
    text_ = (
        f"Country: {country.capitalize()}\n"
        f"Mentor: {', '.join([m[0] for m in mentors]) or 'Unknown'}\n"
        f"Webinar date: {webinar_date}\n"
        f"Webinar time: {webinar_time}\n"
        f"Full name: {user_data.get('fullname')}\n"
        f"Phone number: {user_data.get('phone')}\n"
        f"Degree: {user_data.get('degree', 'Not specified').capitalize()}\n"
        f"Telegram username: @{message.from_user.username or 'Not available'}\n"
        f"Rating: ⭐️{rate}\n"
        f"Feedback: {feedback_text}"
    )
    await bot.send_message(GROUP_CHAT_ID, text_, message_thread_id=WEBINAR_THREAD_FEEDBACK)

    # 🔄 JSON faylga feedback saqlash
    update_user_feedback_in_webinar_file(user_id, feedback_text)

    # ✅ Foydalanuvchiga javob
    if lang in ("en", "english"):
        text_lines = [
            "✅ Thank you for your feedback!\n",
            "We recommend you to book a consultation with our mentor(s):"
        ]
        for name, url in mentors:
            text_lines.append(f"👉 <a href=\"{url}\">{name}</a>")
        await message.answer("\n".join(text_lines), parse_mode="HTML")

    else:
        if mentors:
            text = (
                f"{country.capitalize()}\n"
                f"Sizni mentorimiz <b>{mentors[0][0]}</b> bilan konsultatsiyaga yozilishni tavsiya qilamiz!\n"
                f"👉 <a href=\"{mentors[0][1]}\">Konsultatsiyaga yozilish</a>"
            )
            await message.answer(f"✅ Fikringiz uchun rahmat!\n\n{text}", parse_mode="HTML")
        else:
            await message.answer("✅ Fikringiz uchun rahmat!", parse_mode="HTML")

    await state.finish()







# @dp.callback_query_handler(lambda c: c.data == 'help', state='*')
# async def handler_help(callback: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     lang = data.get('lang', 'uz')
#     print(lang, 354)

    # 🔗 Rasm URL yoki fayl (bu sizda mavjud bo'lishi kerak!)


import aiohttp
from aiogram.types import InputFile
import tempfile
import json
import os


FILE_ID_CACHE = "file_id_cache.json"

def load_file_id():
    if os.path.exists(FILE_ID_CACHE):
        with open(FILE_ID_CACHE, "r") as f:
            return json.load(f)
    return {}

def save_file_id(file_id: str):
    with open(FILE_ID_CACHE, "w") as f:
        json.dump({"image_help": file_id}, f)

@dp.callback_query_handler(lambda c: c.data == 'help', state='*')
async def handler_help(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang_ = data.get('lang', None)
    print(lang_, 591)
    await state.update_data(lang=lang_)
    caption = "."
    if lang_ in ('english','en'):
        caption = (
            "What kind of application do you have?"
        )
    if lang_ in ('uzbek','uz'):
        caption = (
            "Sizning arizangiz qanaqa ko'rinishda?"
        )
    # caption = (
    #     "What kind of application do you have?"
    #     if lang_ in ("en", "english")
    #     else "Sizning arizangiz qanaqa ko'rinishda?"
    # )

    # 🔍 Avval keshdan file_id izlaymiz
    file_id_data = load_file_id()
    if file_id := file_id_data.get("image_help"):
        await callback.message.answer_photo(
            photo=file_id,
            caption=caption,
            reply_markup=get_feedback_buttons(lang_)
        )
        return

    # 🌐 URL'dan rasm yuklab olish
    image_url = "https://demoapi.iapply.org/uni_gallery/78f6836b-480a-4553-a9e4-f16f6750a3d2.png"
    file_image_id = "AgACAgIAAxkBAAEd_udoBinOG-Z_0LcqnS_8fLzTMY4jSQAC_uwxGztkMEgjlad5CxfliAEAAwIAA3kAAzYE"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(await resp.read())
                        tmp_path = tmp_file.name

                    input_photo = InputFile(tmp_path)
                    msg = await callback.message.answer_photo(
                        photo=input_photo,
                        caption=caption,
                        reply_markup=get_feedback_buttons(lang_)
                    )

                    # 🧠 Saqlab qo‘yamiz file_id ni
                    file_id = msg.photo[-1].file_id
                    save_file_id(file_id)
                else:
                    await callback.message.answer("❌ Rasmni yuklab bo‘lmadi. Status:", resp.status)
    except Exception as e:
        await callback.message.answer(f"❌ Xatolik: {str(e)}")






@dp.callback_query_handler(lambda text: text.data in ['shikoyat', 'konsultatsiya'], state="*")
async def fetch_help(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()  # ⚠️ Tugma ishlashi uchun kerak

    data = callback.data
    print(data)
    await state.update_data(type_application=data)

    user_data = await state.get_data()
    lang = user_data.get("lang", None)  # default lang

    print(lang, 644)
    msg = "."
    if lang in ("uzbek", "uz"):
        msg = "To‘liq ism familiyangizni kiriting:"
    if lang in ("english", "en"):
        msg = "Please enter your full name:"

    await callback.message.answer(msg)
    await HelpForm.fullname.set()




@dp.message_handler(state=HelpForm.fullname)
async def fetch_phone(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(fullname=full_name)

    data = await state.get_data()
    lang = data.get("lang", "uz")

    if lang == "uzbek" or lang == "uz":
        text = "☎️ Telefon raqamingizni yuboring."
        request_phone = request_phone_uz
    else:
        text = "☎️ Please send your phone number."
        request_phone = request_phone_en

    await message.answer(text, reply_markup=request_phone)
    await HelpForm.phone.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=HelpForm.phone)
async def fetch_application(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone=phone_number)

    data = await state.get_data()
    type_application = data.get("type_application", None)
    if type_application == "shikoyat":
        lang = data.get("lang", "uz")

        if lang == "english":
            text = "Tell us about your problem in as much detailed way as possible and send us pictures if needed. Try to fit everything in one message 🙏"
        else:
            text = "Muammoingiz haqida iloji boricha batafsil aytib bering va agar kerak bo'lsa, bizga rasmlarni yuboring. Hamma narsani bitta xabarga sig'dirishga harakat qiling 🙏"

        await message.answer(text)


        await HelpForm.application_type.set()  # yoki: await HelpForm.application_text.set()
    else:
        lang = data.get("lang", "uz")

        if lang == "english":
            text = "Send your message"
        else:
            text = "Xabaringizni qoldiring"

        await message.answer(text)


        await HelpForm.application_type.set()

@dp.message_handler(state=HelpForm.application_type)
async def finish_(message: types.Message, state: FSMContext):
    user_text = message.text
    data = await state.get_data()
    lang = data.get("lang", "uz")

    # Guruhga yuboriladigan matn — bu doim inglizcha yoki administratorga mos bo‘lishi mumkin,
    # lekin kerak bo‘lsa, type_application qiymatini ham tarjima qilish mumkin:
    type_application_map = {
    "uz": {
        # "taklif": "Taklif",
        "shikoyat": "Appeal",
        "konsultatsiya": "Consultation"
    },
    "en": {
        # "taklif": "Suggestion",
        "shikoyat": "Appeal",
        "konsultatsiya": "Consultation"
    }
    }

    type_key = data.get('type_application')
    lang_ = lang if lang in type_application_map else "uz"
    type_label = type_application_map[lang_].get(type_key, type_key)

    msg_text = (
        f"#{type_label}\n"
        f"Full name: {data.get('fullname')}\n"
        f"Phone number: {data.get('phone')}\n"
        f"Telegram username: @{message.from_user.username or 'Not available'}\n"
        f"Feedback: {user_text}"
    )


    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=msg_text,
        message_thread_id=WEBINAR_THREAD_ID_HELP,
        parse_mode=None  # ✅ Markdown emas, oddiy text
    )

    data = {
        'usa': "https://iapply.org/mentor/profile/mahliyo-shavkatova-17?application=",
        "germany": "https://iapply.org/mentor/profile/adhambek-yashnarbekov-20?application=",
        "italy": "https://iapply.org/mentor/profile/abdurakhmon-jumanazarov-18?application=,https://iapply.org/mentor/profile/shohjahon-jonmirzayev-19?application=",
        "turkey": "https://iapply.org/mentor/profile/gulbanu-turganbaeva-21?application=",
        "nordic": "https://iapply.org/mentor/profile/shohjahon-jonmirzayev-19?application=",
    }
    mentor_link_text_2 = t('mentor_post_2', lang)
    mentor_link_text_1 = t('mentor_post_1', lang)
    # Foydalanuvchiga chiqadigan javob
    if lang == "english":
        response = "✅ Thank you! We will contact you very soon!"
    else:
        response = "Fikr-mulohazangiz uchun rahmat! Tez orada javob beramiz 😇"

    await message.answer(response, reply_markup=ReplyKeyboardRemove())
    # await state.finish()


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


from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from pathlib import Path

EXCEL_FILE = Path("data/webinar_export.xlsx")
from data.config import ADMINS  # 🛡 O‘zingizning admin ID larni shu yerga yozing

@dp.message_handler(commands=["excel"])
async def handle_export_command(message: types.Message):
    print(message.from_user.id, ADMINS)

    if str(message.from_user.id) not in ADMINS:
        await message.answer("❌ Sizda ushbu buyruqdan foydalanish huquqi yo‘q.")
        return

    if not EXCEL_FILE.exists():
        await message.answer("❌ Excel fayli topilmadi.")
        return

    await message.answer_document(
        document=InputFile(EXCEL_FILE),
        caption="📁 Bu foydalanuvchilar ro'yxati (Excel)"
    )
