from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from app.bot.services import api_requests as api_rq


class AccessFunction(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ):
        user_tg_id = event.from_user.id
        user_products = await api_rq.get_user_product_codes(user_tg_id)

        data['user_products'] = user_products

        return await handler(event, data)