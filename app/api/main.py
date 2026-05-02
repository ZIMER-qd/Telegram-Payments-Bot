from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import (product_router, purchases_router,
                             sub_router, user_router)
from app.database.models import init_db, engine
from app.database.create_products import seed_products
from app.database.seed import products
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logging.info("Database initialized")
    except Exception as e:
        logging.warning(f"Database initialization failed: {e}")

    await seed_products(products)

    yield

    await engine.dispose()
    logging.info("Database connections closed")


app = FastAPI(lifespan=lifespan)

app.include_router(product_router)
app.include_router(purchases_router)
app.include_router(sub_router)
app.include_router(user_router)