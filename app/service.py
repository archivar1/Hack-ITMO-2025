from typing import Optional
from uuid import UUID
from app.utils.database_mock import DatabaseMock
from app.fatsecret_service_mock import FatSecretServiceMock
from app.human_api_service_mock import HumanApiServiceMock
from app.models import CaloriesResponse


class MainService:
    def __init__(self):
        self.db = DatabaseMock()
        self.fatsecret = FatSecretServiceMock()
        self.human_api = HumanApiServiceMock()

    async def start_user(self, user_id: UUID, chat_id: UUID):
        user = await self.db.get_user(user_id)
        if not user:
            await self.db.create_user(user_id, chat_id)

    async def product_count_manual(self, user_id: UUID, product_name: str, calories_burned: int) -> Optional[float]:
        product_info = self.fatsecret.get_calories(product_name)
        if not product_info:
            return None
        if product_info.calories == 0:
            return None
        return calories_burned / product_info.calories

    async def product_count(self, user_id: UUID, days: Optional[int] = None) -> Optional[float]:
        user = await self.db.get_user(user_id)
        if not user:
            return None

        product = await self.db.get_product(user.curr_product_id)
        if not product:
            return None

        calories_burned = self.human_api.get_calories_burned(product.name)
        if calories_burned is None:
            return None

        multiplier = days if days else 1
        total_calories = calories_burned * multiplier

        if product.calories == 0:
            return None
        return total_calories / product.calories

    async def change_product(self, user_id: UUID, product_name: str) -> bool:
        product_info = self.fatsecret.get_calories(product_name)
        if not product_info:
            return False

        if not await self.db.exist_product(product_name):
            product = await self.db.create_product(product_name, int(product_info.calories))
        else:
            for p in self.db.products.values():
                if p.name == product_name:
                    product = p
                    break

        await self.db.update_user_product(user_id, product.id)
        return True

    async def add_custom_product(self, user_id: UUID, product_name: str, calories: int) -> bool:
        try:
            await self.db.create_product(product_name, calories)
            return True
        except:
            return False

    async def get_product(self, user_id: UUID) -> Optional[str]:
        user = await self.db.get_user(user_id)
        if not user:
            return None

        product = await self.db.get_product(user.curr_product_id)
        if not product:
            return None

        return f"{product.name} - {product.calories} ккал/100г"
