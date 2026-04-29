from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductOut(BaseModel):
    id: int
    code: str
    name: str
    type: str
    price: int
    duration_days: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CheckUserProduct(BaseModel):
    value: bool


class UserProductCodes(BaseModel):
    code: str

    model_config = ConfigDict(from_attributes=True)