from app.database.models import async_session
from app.database.models import User, Subscription, Product, UserProduct

from sqlalchemy import delete, select

from typing import List

import logging


async def set_user(tg_id: int, name: str) -> None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            
            if not user:
                result = User(
                    tg_id=tg_id,
                    name=name
                )
                session.add(result)


async def add_user_product(tg_id: int, product_code: str, expire: str=None) -> None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User.id).where(User.tg_id == tg_id))
            product_id = await session.scalar(select(Product.id).where(Product.code == product_code))
            result = UserProduct(
                user_id=user,
                product_id=product_id,
                expire_at=expire
            )
            session.add(result)