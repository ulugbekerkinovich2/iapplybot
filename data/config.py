from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
GROUP_CHAT_ID = env.int("GROUP_CHAT_ID")
# THREAD_ID = env.int("THREAD_ID")
WEBINAR_THREAD_ID = env.int("WEBINAR_THREAD_ID")
WEBINAR_THREAD_ID_HELP = env.int("WEBINAR_THREAD_ID_HELP")