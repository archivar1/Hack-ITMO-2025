import uuid
from sqlalchemy import UUID, Column, String, Integer, ForeignKey
from app.database import DeclarativeBase


class CustomProduct(DeclarativeBase):
    __tablename__ = "custom_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)


