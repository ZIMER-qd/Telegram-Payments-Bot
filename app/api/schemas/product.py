from pydantic import BaseModel


class AddUserProduct(BaseModel):
    tg_id: int
    product_code: str
    expire: int | None