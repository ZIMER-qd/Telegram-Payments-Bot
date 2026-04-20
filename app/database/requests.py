from app.database.models import async_session
from app.database.models import User, Product, UserProduct

from sqlalchemy import delete, select
from datetime import datetime, timezone, timedelta
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
    if expire:
        now_utc = datetime.now(timezone.utc)
        future = now_utc + timedelta(days=expire)

    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User.id).where(User.tg_id == tg_id))
            product_id = await session.scalar(select(Product.id).where(Product.code == product_code))
            result = UserProduct(
                user_id=user,
                product_id=product_id,
                expire_at=future if expire else None
            )
            session.add(result)


async def check_product_by_user(tg_id: int, product_code: str) -> bool:
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        product_id = await session.scalar(select(Product.id).where(Product.code == product_code))
        result = await session.scalar(select(UserProduct)
                                      .where(UserProduct.user_id == user_id)
                                      .where(UserProduct.product_id == product_id))
        if result:
            return True
        return None
    

async def get_all_products_by_type(type_name: str) -> List[Product]:
    async with async_session() as session:
        result = await session.execute(select(Product).where(Product.type == type_name))
        return result.scalars().all()


async def get_product_by_code(code: str) -> List[Product]:
    async with async_session() as session:
        price = await session.scalar(select(Product).where(Product.code == code))
        return price
    

async def get_user_product_codes(tg_id: int) -> List[UserProduct]:
    async with async_session() as session:
        
        products = (
            select(Product.code)
            .join(UserProduct)
            .join(User)
            .where(User.tg_id == tg_id)
        )

        result = await session.scalars(products)
        return result.all()