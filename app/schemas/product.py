from uuid import UUID

from pydantic import BaseModel, Field

class ProductCreateForm(BaseModel):
    name: str = Field(unique=True)
    calories: int = Field(default=1)
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Must not be blank")
        forbidden_chars = ["&","<",">", '"', "'"]
        if any(char in v for char in forbidden_chars):
            raise ValueError("forbidden character(s)")
        raise v.strip()

