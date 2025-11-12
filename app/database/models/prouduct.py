import uuid
from sqlalchemy import UUID, Column, String, Integer, ForeignKey
from app.database import DeclarativeBase


class Product(DeclarativeBase):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    calories = Column(Integer, nullable=False)


