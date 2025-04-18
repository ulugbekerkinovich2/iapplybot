from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    fullname = State()
    phone = State()
    description = State()
    webinar = State()
    introduce_webinar = State()
    select_webinar = State()
    register_webinar = State()
    collect_opinion = State()
    support_webinar = State()
    ask_degree = State()


class WebinarRegistration(StatesGroup):
    selecting = State()
    full_name = State()
    phone = State()
    telegram_username = State()

    
class HelpForm(StatesGroup):
    application_type = State()
    fullname = State()
    phone = State()
    application = State()

