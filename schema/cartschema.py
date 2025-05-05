from pydantic import BaseModel, Field

class CartItem(BaseModel):
    user_id: int = Field(...)
    product_id: int = Field(...)
    quantity: int = Field(...)
