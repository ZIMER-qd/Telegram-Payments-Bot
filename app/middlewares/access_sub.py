from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from app.database import requests as rq
from datetime import datetime, timezone


class SubVerify(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ):
        user_tg_id = event.from_user.id
        user_sub = await rq.get_user_purchases(user_tg_id)
        now_utc = datetime.now(timezone.utc)
        
        is_active = bool(user_sub[1]) and now_utc <= user_sub[1]
        
        data["is_sub_active"] = is_active

        return await handler(event, data)