from app.api_clients import FatSecretAPI, HumanAPI
from app.database import Database
from app.models import Product


class MainService:
    def __init__(self):
        self.fat_secret = FatSecretAPI()
        self.human_api = HumanAPI()
        self.db = Database()

    def register_user(self, user_id: int):
        if not self.db.user_exists(user_id):
            return self.db.create_user(user_id)
        return self.db.get_user(user_id)

    def add_custom_product(self, user_id: int, product_name: str, calories: float):
        product = Product(name=product_name, calories=calories)
        return self.db.set_product(user_id, product)

    def change_product(self, user_id: int, product_name: str):
        product = self.search_product(product_name)
        self.db.set_product(user_id, Product(name=product_name, calories=product.get("calories")))

    def get_info(self, user_id: int, days: int = 7):
        activity = self.get_user_activity(user_id, days)
        product = self.db.get_product(user_id)

        if not product:
            raise ValueError("Product not set for user")

        if product.calories <= 0:
            raise ValueError("Invalid product calories")

        calories_burned = activity.get("calories_burned", 0)
        product_count = calories_burned / product.calories
        return {
            "calories_burned": calories_burned,
            "product_count": product_count
        }

    def search_product(self, query: str):
        return self.fat_secret.search_product(query)

    def get_user_activity(self, user_id: int, days: int = 1):
        return self.human_api.get_activity_data(user_id, days)

    def add_product_to_user(self, user_id: int, product_data: dict):
        return self.db.add_product_to_user(user_id, product_data)
