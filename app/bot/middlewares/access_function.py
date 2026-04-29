from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from app.database import requests as rq


class AccessFunction(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ):
        user_tg_id = event.from_user.id
        user_products = await rq.get_user_product_codes(user_tg_id)

        data['user_products'] = set(user_products)

        return await handler(event, data)