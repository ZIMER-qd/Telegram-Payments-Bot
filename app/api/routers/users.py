from fastapi import APIRouter, HTTPException, Depends, status
from app.api.schemas import user
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.core.create_asyncsession import get_db

from app.api.services import requests as rq


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/add")
async def create_user(data: user.User, db : AsyncSession = Depends(get_db)) -> dict:
    user = await rq.get_user(db, data.tg_id)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    
    await rq.set_user(db, data.tg_id, data.name)
    return {"success": True}