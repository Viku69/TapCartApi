from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    qr_code: str
    department_id: int


class Product(BaseModel):
    id: int
    name: str
    price: float
    qr_code: str
    department_id: int
