from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.core.create_asyncsession import get_db

router = APIRouter(prefix="/sub", tags=["Subscriptions"])


@router.delete("/del")
async def delete_user_sub(tg_id: int, db : AsyncSession = Depends(get_db)):
    ...