from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Numeric, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine

from datetime import datetime, timezone
from config import config


DB_URL = f"postgresql+asyncpg://postgres:{config.postgre_pass.get_secret_value()}@localhost:5432/mydatabase"

engine = create_async_engine(url=DB_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                 default=lambda: datetime.now(timezone.utc))

    products = relationship('UserProduct', back_populates='user')


class Product(Base):
    __tablename__ = 'Products'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Numeric(10, 2))
    duration_days: Mapped[int] = mapped_column(Integer, nullable=True)


class UserProduct(Base):
    __tablename__ = 'User Products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('Products.id'))
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                   default=lambda: datetime.now(timezone.utc))
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship('User', back_populates='products')
    product = relationship('Product')


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)