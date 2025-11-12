from typing import Optional
from uuid import UUID
from app.mocks import DatabaseMock, FatSecretServiceMock, HumanApiServiceMock
from app.models import CaloriesResponse


class MainService:
    def __init__(self):
        self.db = DatabaseMock()
        self.fatsecret = FatSecretServiceMock()
        self.human_api = HumanApiServiceMock()

    async def get_or_create_user_by_chat_id(self, chat_id: int) -> UUID:
        user = await self.db.get_user_by_chat_id(chat_id)
        if not user:
            user = await self.db.create_user(chat_id)
        return user.id

    async def start_user(self, chat_id: int):
        await self.get_or_create_user_by_chat_id(chat_id)

    async def product_count_manual(self, user_id: UUID, product_name: str, calories_burned: int) -> Optional[float]:
        product_info = self.fatsecret.get_calories(product_name)
        if not product_info:
            return None
        if product_info.calories == 0:
            return None
        return calories_burned / product_info.calories

    async def product_count(self, user_id: UUID, days: Optional[int] = None) -> Optional[dict]:
        user = await self.db.get_user(user_id)
        if not user:
            return None

        product = await self.db.get_product(user.curr_product_id)
        if not product:
            return None

        calories_burned = self.human_api.get_calories_burned(days)
        if calories_burned is None:
            return None

        multiplier = days if days else 1
        total_calories = calories_burned * multiplier

        if product.calories == 0:
            return None

        amount = total_calories / product.calories
        return {
            "amount": amount,
            "product_name": product.name,
            "calories": product.calories
        }

    async def change_product(self, user_id: UUID, product_name: str) -> bool:
        if await self.db.exist_product(product_name):
            product = await self.db.get_product_by_name(product_name)
            await self.db.update_user_product(user_id, product.id)
            return True

        product_info = self.fatsecret.search_food(product_name)
        if not product_info:
            return False

        product = await self.db.create_product(product_info['food_name'], int(product_info['calories']))
        await self.db.update_user_product(user_id, product.id)
        return True

    async def add_custom_product(self, user_id: UUID, product_name: str, calories: int) -> bool:
        try:
            await self.db.create_product(product_name, calories)
            return True
        except:
            return False

    async def get_product(self, user_id: UUID) -> Optional[dict]:
        user = await self.db.get_user(user_id)
        if not user:
            return None

        product = await self.db.get_product(user.curr_product_id)
        if not product:
            return None

        return {
            "name": product.name,
            "calories": product.calories
        }
