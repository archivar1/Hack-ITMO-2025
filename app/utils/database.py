from typing import Dict, Optional, AsyncGenerator
from uuid import UUID
from sqlalchemy.sql.annotation import Annotated
from app.database.models import User, Product
from app.database.connection import get_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class Database:

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with get_session() as session:
            try:
                yield session
            finally:
                await session.close()

    async def get_user(self, user_id: int) -> Optional[User]:
        async for session in get_session():
            try:
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                curr_user = result.scalar_one_or_none()
                return curr_user
            except Exception as e:
                await session.rollback()
                raise (f"Error getting user with id {user_id}")

    async def create_user(self, user_id: UUID, chat_id: UUID) -> Optional[User]:
        async for session in get_session():
            query = select(Product).where(Product.name == 'Beer')
            result = await session.execute(query)
            default_product_id = result.scalar_one_or_none()
            user = User(chat_id=chat_id, curr_product_id=default_product_id)

            session.add(user)
            try:
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError:
                await session.rollback()

    async def exist_product(self, product_name: str) -> bool:
        async for session in get_session():
            query = select(Product).where(Product.name == product_name)
            result = (await session.execute(query)).scalar_one_or_none()
            if result:
                return False
            return True
        return False

    async def create_product(self, product_name: str) -> Optional[Product]:
        if self.exist_product(product_name):
            raise Exception("Product already exists")
        async for session in get_session():
            product = session.add(Product(name=product_name))
            try:
                await session.commit()
                await session.refresh(product)
                return product
            except IntegrityError:
                await session.rollback()
                raise (f"Error creating product with name {product_name}, product already exists")

    async def get_product(self, product_id: int) -> Optional[Product]:
        async for session in get_session():
            try:
                query = select(Product).where(Product.id == product_id)
                result = await session.execute(query)
                curr_product = result.scalar_one_or_none()
                return curr_product
            except Exception as e:
                await session.rollback()
                raise (f"Error getting product with id {product_id}")
