from uuid import UUID

from pydantic import BaseModel, Field

class ProductCreateForm(BaseModel):
    name: str = Field(unique=True)
    calories: int = Field(default=1)
