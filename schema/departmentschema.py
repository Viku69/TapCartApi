from pydantic import BaseModel, Field


class DepartmentCreate ( BaseModel):
    name: str