from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from app.bot.services import api_requests as api_rq
from datetime import datetime, timezone


class SubVerify(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ):
        user_tg_id = event.from_user.id
        user_sub = await api_rq.get_user_purchases(user_tg_id)

        if user_sub is None:
            data['is_sub_active'] = False
            return await handler(event, data)
        
        now_utc = datetime.now(timezone.utc)
        expire = datetime.fromisoformat(user_sub["subscription"].replace('Z', '+00:00'))

        if expire and expire.tzinfo is None:
            expire = expire.replace(tzinfo=timezone.utc)

        is_active = bool(user_sub["subscription"]) and now_utc <= expire
        
        if not is_active:
            await api_rq.delete_user_sub(event.from_user.id)

        data["is_sub_active"] = is_active

        return await handler(event, data)