from uuid import UUID
from pydantic import BaseModel, Field

class User(BaseModel):
    id: UUID
    chat_id: str