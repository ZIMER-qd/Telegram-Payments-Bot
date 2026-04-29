from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.api.schemas.product_ouput import ProductOut


class UserPurchasesOut(BaseModel):
    products: List[ProductOut]
    expire: Optional[datetime] = None