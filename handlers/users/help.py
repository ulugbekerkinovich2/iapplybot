from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils.lang import t
from data.config import WEBINAR_THREAD_ID, GROUP_CHAT_ID
from states.userState import HelpForm


def get_lang(data: dict, message: types.Message) -> str:
    """
    Foydalanuvchi tilini olish uchun universal funksiya.
    """
    lang = data.get("lang")
    if lang not in ["uz", "en"]:
        print(message.from_user.language_code[:2])
        lang = message.from_user.language_code[:2] if message.from_user.language_code else "uz"
    elif lang == 'ru':
        lang = 'en'
    elif lang not in ["uz", "en"]:
        lang = "uz"
    return lang


@dp.message_handler(commands=["help"], state="*")
async def help_command(message: types.Message, state: FSMContext):
    print('help ishga tushdi')
    data = await state.get_data()
    lang = get_lang(data, message)

    await message.answer(
        f"{t('help', lang)}\n\n{t('ask_your_question', lang)}",
        parse_mode="HTML"
    )
    await HelpForm.waiting_for_help_text.set()


# @dp.message_handler(state=HelpForm.waiting_for_help_text)
# async def receive_help_text(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     lang = get_lang(data, message)

#     user = message.from_user
#     text = message.text.strip().lower()

#     # Buyruqlarni bloklash
#     if text in ["/start", "/help", "start", "help"]:
#         return

#     log_text = (
#         f"🆘 <b>{t('help_request', lang)}</b>\n"
#         f"👤 <b>{t('user', lang)}:</b> {user.full_name} (@{user.username or 'yo‘q'})\n"
#         f"🆔 <b>ID:</b> {user.id}\n"
#         f"✉️ <b>{t('message', lang)}:</b> {message.text}"
#     )

#     try:
#         await bot.send_message(
#             chat_id=GROUP_CHAT_ID,
#             text=log_text,
#             message_thread_id=WEBINAR_THREAD_ID,
#             parse_mode="HTML"
#         )
#     except Exception:
#         await bot.send_message(
#             chat_id=GROUP_CHAT_ID,
#             text=log_text,
#             parse_mode="HTML"
#         )

#     await message.answer(t("help_sent", lang))
#     await state.finish()
