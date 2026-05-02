from app.database.models import async_session
from app.database.models import User, Product, UserProduct

from sqlalchemy import delete, select
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(session: AsyncSession, tg_id: int) -> bool:
    """Get user from database.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.

    Returns:
        _type_: False if user not exist otherwise True.
    """

    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        return False
    
    return True


async def set_user(session: AsyncSession, tg_id: int, name: str) -> None:
    """Create user in the database.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.
        name (str): User first name.
    
    Returns:
        The function does not return anything. 
    """

    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    
    if not user:
        result = User(
            tg_id=tg_id,
            name=name
        )
        session.add(result)
        await session.commit()
    

async def add_user_product(session: AsyncSession, tg_id: int, product_code: str, expire: int=None) -> None:
    """Create user product in the database.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.
        product_code (str): Product code.
        expire (str, optional): Time when the product runs out. Defaults to None.

    Returns:
        The function does not return anything.
    """

    future = None
    if expire:
        now_utc = datetime.now(timezone.utc)
        future = now_utc + timedelta(days=expire)

    async with session.begin():
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        product = await session.scalar(select(Product).where(Product.code == product_code))
        
        if product.type == 'subscription':
            user_sub = await session.scalar(select(UserProduct)
                                            .join(Product)
                                            .where(UserProduct.user_id == user_id)
                                            .where(Product.type == 'subscription'))
            
            if user_sub:
                expire_at = user_sub.expire_at

                if expire_at and expire_at.tzinfo is None:
                    expire_at = expire_at.replace(tzinfo=timezone.utc)
                    
                user_sub.expire_at = user_sub.expire_at + timedelta(days=expire)
            else:
                session.add(UserProduct(
                    user_id=user_id,
                    product_id=product.id,
                    expire_at=future
                ))
        else:
            session.add(UserProduct(
                user_id=user_id,
                product_id=product.id,
                expire_at=future if expire else None
            ))


async def check_product_by_user(session: AsyncSession, tg_id: int, product_code: str) -> bool:
    """Checking whether the user has the product.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.
        product_code (str): Product code.

    Returns:
        bool: True if available otherwise None.
    """

    user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
    product_id = await session.scalar(select(Product.id).where(Product.code == product_code))
    result = await session.scalar(select(UserProduct)
                                    .where(UserProduct.user_id == user_id)
                                    .where(UserProduct.product_id == product_id))
    if result:
        return True
    
    return False
    

async def get_all_products_by_type(session: AsyncSession, type_name: str) -> List[Product]:
    """Get all products by type

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        type_name (str): Product type.

    Returns:
        List[Product]: A list of Product objects matching the specified type.
    """

    result = await session.execute(select(Product).where(Product.type == type_name))
    return result.scalars().all()


async def get_product_by_code(session: AsyncSession, code: str) -> Product:
    """Get product by code.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        code (str): Product code.

    Returns:
        Product: Product instance.
    """

    product = await session.scalar(select(Product).where(Product.code == code))
    return product
    

async def get_user_product_codes(session: AsyncSession, tg_id: int) -> List[str]:
    """Get all product codes.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.

    Returns:
        List[UserProduct]: List of product codes.
    """

    products = (
        select(Product.code)
        .join(UserProduct)
        .join(User)
        .where(User.tg_id == tg_id)
    )

    result = await session.scalars(products)
    return result.all()
    

async def get_user_purchases(session: AsyncSession, tg_id: int) -> tuple[List[Product], Optional[datetime]]:
    """Retrieve user's purchased products and subscription expiration date.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.

    Returns:
        tuple[List[Product], Optional[datetime]]:
            - List of purchased function products
            - Subscription expiration datetime (if exists)
    """
        
    sub = await session.scalar(
        select(UserProduct.expire_at)
        .join(Product)
        .join(User)
        .where(User.tg_id == tg_id)
        .where(Product.type == 'subscription')
    )

    funcs = (await session.scalars(
        select(Product)
        .join(UserProduct)
        .join(User)
        .where(User.tg_id == tg_id)
        .where(Product.type == 'function')
    )).all()

    return (funcs, sub) 


async def delete_user_sub(session: AsyncSession, tg_id: int) -> None:
    """Deletes a user's subscription.

    Args:
        session (AsyncSession): SQLAlchemy async session for working with a database.
        tg_id (int): Telegram user ID.

    Returns:
        The function does not return anything.
    """

    user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
    product_ids = (await session.scalars(select(Product.id).where(Product.code.startswith('sub')))).all()

    result = (
        delete(UserProduct)
        .where(UserProduct.user_id == user_id)
        .where(UserProduct.product_id.in_(product_ids)))

    await session.execute(result)
    await session.commit()