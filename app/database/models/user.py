import uuid
from sqlalchemy import UUID, Column, Integer, ForeignKey
from app.database import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True, index=True)
    curr_product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, chat_id={self.chat_id}, curr_product_id={self.curr_product_id})"
