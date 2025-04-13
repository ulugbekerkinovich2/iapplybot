from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_kb = InlineKeyboardMarkup(row_width=1)  # 👈 Har tugma alohida qatorda chiqadi


def get_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    if lang == "english":
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📤 Submit Application", callback_data="help"),
            InlineKeyboardButton("📝 Register for Webinar", callback_data="register_webinar"),
            InlineKeyboardButton("🌐 Change Language", callback_data="change_language")
        )
    else:
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📤 Ariza qoldirish", callback_data="help"),
            InlineKeyboardButton("📝 Vebinarga ro'yhatdan o'tish", callback_data="register_webinar"),
            InlineKeyboardButton("🌐 Tilni o'zgartirish", callback_data="change_language")
        )
def get_language_selection_keyboard(current_lang: str = "uz") -> InlineKeyboardMarkup:
    uz_flag = "🇺🇿"
    en_flag = "🇺🇸"

    if current_lang == "uz":
        uz_label = f"{uz_flag} O‘zbek (✅)"
        en_label = f"{en_flag} Ingliz"
    else:
        uz_label = f"{uz_flag} Uzbek"
        en_label = f"{en_flag} English (✅)"

    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(uz_label, callback_data='uzbek'),
        InlineKeyboardButton(en_label, callback_data='english')
    )


language = InlineKeyboardMarkup(row_width=2)
language.add(
    InlineKeyboardButton("🇺🇿 Uzbek", callback_data='uzbek'),
    InlineKeyboardButton("🇺🇸 English", callback_data='english')
)

country_kb = InlineKeyboardMarkup(row_width=2)
country_kb.add(
    InlineKeyboardButton("🇮🇹Italy", callback_data='italy'),
    InlineKeyboardButton("🇹🇷Turkey", callback_data='turkey'),
    InlineKeyboardButton("🇫🇮/🇳🇴/🇸🇪/🇨🇭\nNordic Countries", callback_data='nordic')
)
country_kb.add(

    InlineKeyboardButton("🇩🇪Germany", callback_data='germany'),
    InlineKeyboardButton("🇰🇷South Korea", callback_data='korea'),
    InlineKeyboardButton("🇺🇸USA", callback_data='usa'),
    InlineKeyboardButton("🇭🇺Hungary", callback_data='hungary'),
)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_country_keyboard(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)

    if lang == "english":
        kb.add(
            InlineKeyboardButton("🇹🇷 Turkey", callback_data="turkey"),
            InlineKeyboardButton("🇩🇪 Germany", callback_data="germany"),
            InlineKeyboardButton("🇺🇸 USA", callback_data="usa"),
            InlineKeyboardButton("🇮🇹 Italy", callback_data="italy"),
            InlineKeyboardButton("🇰🇷 South Korea", callback_data="korea"),
            InlineKeyboardButton("🇭🇺 Hungary", callback_data="hungary")
        )
        kb.add(
            InlineKeyboardButton("🇫🇮 / 🇳🇴 / 🇸🇪 / 🇨🇭 Nordic Countries", callback_data="nordic")
        )
        kb.add(
            InlineKeyboardButton("❌ Cancel", callback_data="cancel")
        )
    else:
        kb.add(
            InlineKeyboardButton("🇹🇷 Turkiya", callback_data="turkey"),
            InlineKeyboardButton("🇩🇪 Germaniya", callback_data="germany"),
            InlineKeyboardButton("🇺🇸 AQSH", callback_data="usa"),
            InlineKeyboardButton("🇮🇹 Italiya", callback_data="italy"),
            InlineKeyboardButton("🇰🇷 Janubiy Koreya", callback_data="korea"),
            InlineKeyboardButton("🇭🇺 Hungary", callback_data="hungary")
        )
        kb.add(
            InlineKeyboardButton("🇫🇮 / 🇳🇴 / 🇸🇪 / 🇨🇭 Nordic Davlatlari", callback_data="nordic")
        )
        kb.add(
            InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")
        )

    return kb



def get_mentor_keyboard(country: str, lang: str = "uz") -> InlineKeyboardMarkup:
    inline_mentor = InlineKeyboardMarkup(row_width=1)

    if lang == "english" or lang == "en":
        btn_text = "📤 Register"
    else:
        btn_text = "📤 Ro'yhatdan o'tish"

    inline_mentor.add(
        InlineKeyboardButton(btn_text, callback_data=f"register_consultant:{country}")
    )
    return inline_mentor




def get_select_degree_inline(lang: str) -> InlineKeyboardMarkup:
    if lang == "en" or lang == "english":
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("🎓 Bachelor's", callback_data='bachelor'),
            InlineKeyboardButton("🎓 Master's", callback_data='master'),
            InlineKeyboardButton("❌ Cancel", callback_data='cancel')
        )
    else:
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("🎓 Bakalavr", callback_data='bachelor'),
            InlineKeyboardButton("🎓 Magistr", callback_data='master'),
            InlineKeyboardButton("❌ Bekor qilish", callback_data='cancel')
        )


application_buttons = InlineKeyboardMarkup(row_width=2)
application_buttons.add(
    InlineKeyboardButton("💌 Taklif", callback_data='taklif'),
    InlineKeyboardButton("🚫 Shikoyat", callback_data='shikoyat'),
    InlineKeyboardButton("🧠 Konsultatsiya olish", callback_data='konsultatsiya')
)
def get_feedback_buttons(lang: str) -> InlineKeyboardMarkup:
    if lang == "english" or lang == "en":
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("💌 Suggestion", callback_data='taklif'),
            InlineKeyboardButton("🚫 Complaint", callback_data='shikoyat'),
            InlineKeyboardButton("🧠 Request a consultation", callback_data='konsultatsiya')
        )
    else:
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("💌 Taklif", callback_data='taklif'),
            InlineKeyboardButton("🚫 Shikoyat", callback_data='shikoyat'),
            InlineKeyboardButton("🧠 Konsultatsiya olish", callback_data='konsultatsiya')
        )





def get_feedback_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(*[
        InlineKeyboardButton(text=str(f'⭐️{i}'), callback_data=f"rate_{i}") for i in range(1, 6)
    ])
    return keyboard


sub_buttons = InlineKeyboardMarkup(row_width=1)
sub_buttons.add(
    InlineKeyboardButton("🇺🇿 iApply (UZ)", url="https://t.me/iapplyorguz"),
    InlineKeyboardButton("🇬🇧 iApply (EN)", url="https://t.me/iapplyorg"),
)



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def check_subscription_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("🇺🇿 iApply (Uzb)", url="https://t.me/iapplyorguz"),
            InlineKeyboardButton("🇬🇧 iApply (Eng)", url="https://t.me/iapplyorg")
        ],
        [
            InlineKeyboardButton("✅ Aʼzolikni tekshirish", callback_data="check_subscription")
        ]
    ])
