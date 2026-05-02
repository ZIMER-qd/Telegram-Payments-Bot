from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.api.schemas.product_ouput import ProductOut


class UserPurchasesOut(BaseModel):
    funcs: List[ProductOut]
    subscription: Optional[datetime] = None