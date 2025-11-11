import uuid
from sqlalchemy import UUID, Column, String
from app.database import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    telegram_token = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)


