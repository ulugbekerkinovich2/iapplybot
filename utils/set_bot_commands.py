from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Boshlash"),
            types.BotCommand("webinar", "Vebinar"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("changelanguage", "Tilni o'zgartirish")
        ],
        scope=types.BotCommandScopeDefault()
    )