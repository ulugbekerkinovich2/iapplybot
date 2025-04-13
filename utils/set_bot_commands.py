from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start"),
            types.BotCommand("vebinar", "Vebinar"),
            types.BotCommand("application", "Ariza"),
            types.BotCommand("change_language", "Tilni o'zgartirish")
        ],
        scope=types.BotCommandScopeDefault()
    )