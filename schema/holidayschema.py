
from pydantic import BaseModel

class Holiday(BaseModel):
    date: str   # 'YYYY-MM-DD'
    name: str
