from pydantic import BaseModel, Field
from uuid import UUID

class Order(BaseModel):
    user_id: int = Field(...)
    order_id: UUID = Field(...)
    total_amount: float = Field(...)
    store_id: int = Field(...)
