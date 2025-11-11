from typing import Dict

class FatSecretAPI:
    def search_product(self, product_id: str) -> Dict:
        return {
            "id": product_id,
            "name": "Sample Product",
            "calories": 100
        }


class HumanAPI:
    def get_activity_data(self, user_id: int, days: int = 1) -> Dict:
        return {
            "user_id": user_id,
            "steps": 10000,
            "calories_burned": 500,
        }
