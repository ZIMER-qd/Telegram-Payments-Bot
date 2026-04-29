from fastapi import APIRouter, HTTPException, Depends
from app.api.schemas import product
from app.api.core.create_asyncsession import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.services import requests as rq
from app.api.schemas.product_ouput import CheckUserProduct, ProductOut, UserProductCodes


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/add")
async def create_user_product(data: product.AddUserProduct, db : AsyncSession = Depends(get_db)):
    await rq.add_user_product(db, data.tg_id, data.product_code, data.expire)
    return {"success": True}


@router.get("/by_code", response_model=ProductOut)
async def get_product_by_code(code: str, db : AsyncSession = Depends(get_db)):
    result = await rq.get_product_by_code(db, code)
    
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    return result


@router.get("/check", response_model=CheckUserProduct)
async def check_user_product(tg_id: int, product_code: str, db : AsyncSession = Depends(get_db)):
    result = await rq.check_product_by_user(db, tg_id, product_code)
    return {"value": result}


@router.get("/by_type", response_model=List[ProductOut])
async def get_products_by_type(type_name: str, db : AsyncSession = Depends(get_db)):
    result = await rq.get_all_products_by_type(db, type_name)
    
    if not result:
        raise HTTPException(status_code=404, detail="Products not found")
    
    return result


@router.get("/user/by_codes", response_model=List[UserProductCodes])
async def get_user_product_codes(tg_id: int, db : AsyncSession = Depends(get_db)):
    result = await rq.get_user_product_codes(db, tg_id)
    return result