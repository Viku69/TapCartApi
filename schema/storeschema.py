from pydantic import BaseModel


class StoreCreate(BaseModel):
    name: str
    type: int
    size:int
    location: str
