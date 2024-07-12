import asyncio
import json
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await message.reply("Too many requests!")


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 3, filepath: str = 'user_requests.json'):
        self.limit = limit
        self.filepath = filepath
        super(RateLimitMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = str(message.from_user.id)
        today = datetime.now().strftime("%Y-%m-%d")

        # Load user requests data from JSON file
        try:
            with open(self.filepath, 'r') as file:
                user_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_data = {}

        # Check and update user request count
        if user_id in user_data:
            last_request_date = user_data[user_id].get('last_request_date', None)
            request_count = user_data[user_id].get('request_count', 0)

            if last_request_date == today:
                if request_count >= self.limit:
                    await message.answer("You have reached your daily limit of requests.")
                    raise CancelHandler()
                else:
                    user_data[user_id]['request_count'] += 1
            else:
                user_data[user_id]['request_count'] = 1
                user_data[user_id]['last_request_date'] = today
        else:
            user_data[user_id] = {'request_count': 1, 'last_request_date': today}

        # Save updated user requests data to JSON file
        with open(self.filepath, 'w') as file:
            json.dump(user_data, file)