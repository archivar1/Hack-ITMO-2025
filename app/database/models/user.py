import uuid
from sqlalchemy import UUID, Column, String, ForeignKey
from app.database import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    chat_id = Column(String, nullable=False)
    curr_product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)


