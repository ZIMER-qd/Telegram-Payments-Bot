from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    tg_id: int
    name: str