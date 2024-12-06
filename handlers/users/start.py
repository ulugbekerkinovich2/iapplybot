from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from states.userState import Form
from data.config import GROUP_CHAT_ID, THREAD_ID
from loader import dp, bot
from middlewares.throttling import RateLimitMiddleware
dp.middleware.setup(RateLimitMiddleware())
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await Form.fullname.set()
    await message.answer("👋 Welcome! Please enter your full name:")

# Handle full name input
@dp.message_handler(state=Form.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await Form.next()

    # Send a message with a button to share the phone number
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("📞 Share your phone number", request_contact=True)
    keyboard.add(button)
    await message.answer("Please share your phone number by clicking the button below:", reply_markup=keyboard)

# Handle contact input
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
async def process_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    await Form.next()
    await message.answer("Great! Now, please provide a brief description about your request:", reply_markup=types.ReplyKeyboardRemove())

# Handle description input
@dp.message_handler(state=Form.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    # Send the collected information to the group
    await bot.send_message(
        GROUP_CHAT_ID,
        f"📋 New Form Submission:\n\n"
        f"👤 Full Name: {data['fullname']}\n"
        f"📞 Phone Number: {data['phone']}\n"
        f"📝 Description: {data['description']}",
        message_thread_id=THREAD_ID
    )

    # Finish conversation with the user
    await message.answer("✅ Thank you for the information! our iApply colleagues will contact you soon 😊")
    await state.finish()
