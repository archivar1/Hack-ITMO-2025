from typing import Optional
from uuid import UUID, uuid4
from app.database.models import User, Product


class DatabaseMock:
    def __init__(self):
        self.users = {}
        self.products = {}

        default_product = Product(id=uuid4(), name='Beer', calories=43)
        self.products[default_product.id] = default_product

    async def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    async def create_user(self, user_id: UUID, chat_id: UUID) -> Optional[User]:
        default_product_id = next(iter(self.products.keys()))
        user = User(id=user_id, chat_id=chat_id, curr_product_id=default_product_id)
        self.users[user_id] = user
        return user

    async def exist_product(self, product_name: str) -> bool:
        for product in self.products.values():
            if product.name == product_name:
                return True
        return False

    async def create_product(self, product_name: str, calories: int) -> Optional[Product]:
        if await self.exist_product(product_name):
            raise Exception("Product already exists")
        product = Product(id=uuid4(), name=product_name, calories=calories)
        self.products[product.id] = product
        return product

    async def get_product(self, product_id: UUID) -> Optional[Product]:
        return self.products.get(product_id)

    async def update_user_product(self, user_id: UUID, product_id: UUID):
        if user_id in self.users:
            self.users[user_id].curr_product_id = product_id
