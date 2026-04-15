from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime, timezone
from pathlib import Path

BASE = Path.cwd()
DB_PATH = BASE / 'db.sqlite3'

engine = create_async_engine(url=f'sqlite+aiosqlite:///{DB_PATH}')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                 default=lambda: datetime.now(timezone.utc))


class Subscription(Base):
    __tablename__ = 'Subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    expire_at: Mapped[datetime] = mapped_column(DateTime())


class Product(Base):
    __tablename__ = 'Products'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Numeric(10, 2))


class UserProduct(Base):
    __tablename__ = 'User Products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.id'))
    purchased_at: Mapped[datetime] = mapped_column(DateTime())
    expire_at: Mapped[datetime] = mapped_column(DateTime())


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)