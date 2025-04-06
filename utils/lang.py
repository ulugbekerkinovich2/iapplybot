translations = {
    "uz": {
        "choose_language": "🇺🇿 Tilni tanlang:",
        "welcome": "👋 Xush kelibsiz! Iltimos, to‘liq ismingizni kiriting:",
        "send_phone": "📞 Telefon raqamingizni yuboring:",
        "description_prompt": "📝 Iltimos, qisqacha izoh yozing:",
        "thank_you": "✅ Rahmat! iApply jamoasi siz bilan tez orada bog‘lanadi 😊",
        "check_subscription": "✅ Obunani tekshirish",
        "register_button": "✍️ Ro‘yxatdan o‘tish",
        "select_webinar": " ✨ Ajoyib! Keling, boshlaymiz! ✨\nBizda sizni dunyo universitetlariga hujjat topshirish jarayonida yo‘naltiradigan ajoyib mentorlar bilan vebinarlar mavjud!\n /help - taklif va shikoyatlar uchun",
        "schedule_webinar": "🗓️ Vebinarlar Jadvali:",
        "date": "Date",
        "time": "Time",
        "mentor": "Mentor",
        "topics": "Topics",
        "message_webinar": "📌 Siz bir nechta vebinarlarga ro‘yxatdan o‘tishingiz mumkin! Istalgan vebinarga tanlov qilishingiz mumkin.",
        "ask_select_webinar": "👀 Qaysi vebinarda ishtirok etishni xohlaysiz?\nIltimos, tanlash uchun quyidagi tugmalardan birini bosing.",
        "register_part_webinar": "Foydalanuvchi vebinarni tanlagandan keyin, bot undan kerakli ma’lumotlarni so‘raydi.",
        "congrats_1_webibar": "ni tanlaganingiz uchun tashakkur!",
        "congrats_2_webibar": "\nBiz sizni ro‘yxatdan o‘tkazish uchun bir nechta ma’lumotlarni olishimiz kerak:",
        "participate_webinar": "Vebinarda ishtirok etish",
        "share_phone": "📱 Telefon raqamni yuborish",
        "send_phone": "<b>👉 Telefon raqamingizni yuboring:</b>",
        "ask_username": "👉 <b>Telegram username'ingizni yozing (masalan: @username):</b>",
        "help": "Sizga qanday yordam bera olamiz?\nIltimos, savollaringiz, takliflaringiz yoki shikoyatlaringizni yozib qoldiring!",
        "ask_your_question": "✍️ Savolingizni shu yerga yozing. Adminlar ko‘rib chiqadi.",
        "help_request": "Yordam so‘rovi",
        "user": "Foydalanuvchi",
        "message": "Xabar",
        "help_sent": "✅ Xabaringiz yuborildi. Adminlar tez orada javob berishadi.",
        "congrats": "🎉 <b>Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!</b>\nVebinarga yaqinlashgan sari eslatma va ulanish havolasini olasiz. Kuzatib boring! 😊",
        "ask_name": "👉 To‘liq ismingizni kiriting",
        "webinar_intro": "universitetlariga qanday hujjat topshirish, grantlar olish va viza jarayonlari haqida bilib oling.",
        "congrats_1_webinar": "ni tanlaganingiz uchun tashakkur!",
        "congrats_2_webinar": "\nBiz sizni ro‘yxatdan o‘tkazish uchun bir nechta ma’lumotlarni olishimiz kerak:"



    },
    "en": {
        "congrats_1_webinar": "Thank you for selecting the",
        "congrats_2_webinar": " webinar!\nWe just need a few details to register you:",
        "choose_language": "🇬🇧 Choose your language:",
        "welcome": "👋 Welcome! Please enter your full name:",
        "send_phone": "📞 Please share your phone number:",
        "description_prompt": "📝 Please write a short description:",
        "thank_you": "✅ Thank you! Our iApply team will contact you soon 😊",
        "check_subscription": "✅ Check subscription",
        "register_button": "✍️ Register",
        "select_webinar": " ✨ Great! Let's get started! ✨\nWe have upcoming webinars with amazing mentors who will guide you through the application processes for universities around the world.\n/help - questions and suggestions",
        "schedule_webinar": "🗓️ Webinars Schedule:",
        "data": "Sana",
        "time": "Vaqt",
        "mentor": "Mentor",
        "topics": "Mavzular",
        "message_webinar": "📌 You can register for multiple webinars! Select your desired webinar, and we’ll proceed with registration.",
        "ask_select_webinar": "👀 Which webinar would you like to attend?\nPlease click the button below to select your webinar.",
        "congrats_1_webinar": "Thank you for selecting the",
        "congrats_2_webinar": "\nWe just need a few details to register you:",
        "participate_webinar": "Participate in the webinar",
        "share_phone": "📱 Share your phone number",
        "send_phone": "<b>👉 Send phone number:</b>",
        "ask_username": "👉 <b>Share your Telegram username (e.g., @username):</b>",
        "help": "How can I assist you today?\nPlease let me know if you have any questions, suggestions, or concerns. Feel free to share them below!",
        "ask_your_question": "✍️ Please type your question here. Our admins will review it.",
        "help_request": "Help Request",
        "user": "User",
        "message": "Message",
        "help_sent": "✅ Your message has been sent. Our admins will get back to you shortly.",
        "congrats": "🎉 <b>You've reached your goal!</b>\nYou'll receive a reminder and link as you get closer to the webinar. Stay tuned! 😊\n/help - questions and suggestions",
        "ask_name": "👉 Please provide your full name",
        "each_webinar": "How to apply to Turkish Universities, Scholarships, Visa process.",
        "webinar_intro": "learn how to apply to universities, get scholarships, and understand the visa process.",

    }
}

country_translations = {
    "uz": {
        "Turkey": "Turkiya",
        "USA": "AQSH",
        "UK": "Buyuk Britaniya",
        "Germany": "Germaniya"
    },
    "en": {
        "Turkey": "Turkey",
        "USA": "USA",
        "UK": "United Kingdom",
        "Germany": "Germany"
    }
}

def translate_country(country: str, lang: str) -> str:
    return country_translations.get(lang, {}).get(country, country)

def t(key: str, lang: str = "uz") -> str:
    return translations.get(lang, translations["uz"]).get(key, key)

