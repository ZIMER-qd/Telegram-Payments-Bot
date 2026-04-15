from app.database.models import async_session
from app.database.models import Product

from sqlalchemy import select

import logging


async def seed_products(products: list[dict]) -> None:
    for product in products:
        exists = await get_product_by_code(product['code'])

        if not exists:
            await create_product(**product)


async def get_product_by_code(product: str) -> Product | None:
    async with async_session() as session:
        result = await session.scalar(select(Product).where(Product.code == product))
        return result is not None
    

async def create_product(**kwargs) -> None:
    async with async_session() as session:
        async with session.begin():
            try:
                product = Product(**kwargs)
                session.add(product)
            except Exception as e:
                logging.warning(f"Error creating product: {e}")