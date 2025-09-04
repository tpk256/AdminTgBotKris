from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config_reader import config


class CheckAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = data["event_from_user"].id
        print("USER ID: ", user_id)
        data['is_auth'] = user_id in config.admin_id
        result = await handler(event, data)
        return result