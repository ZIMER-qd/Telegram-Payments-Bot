from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.core.create_asyncsession import get_db
from typing import List

from app.api.services import requests as rq
from app.api.schemas.purchases_ouput import UserPurchasesOut
from app.api.schemas.product_ouput import ProductOut


router = APIRouter(prefix="/purchases", tags=["Parchases"])


@router.get("/user", response_model=UserPurchasesOut)
async def get_user_purchases(tg_id: int, db : AsyncSession = Depends(get_db)):
    funcs, subscription = await rq.get_user_purchases(db, tg_id)
    return {"funcs": funcs, "subscription": subscription}