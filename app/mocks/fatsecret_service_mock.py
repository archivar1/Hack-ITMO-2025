from typing import Optional, Dict, Any
from app.models import CaloriesResponse


class FatSecretServiceMock:
    def get_calories(self, food_name: str) -> Optional[CaloriesResponse]:
        food_name = food_name.lower()
        mock_data = {
            'chicken': CaloriesResponse(
                food_name='Chicken',
                calories=150,
                serving_description='100 г',
                protein=30,
                fat=3.0,
                carbohydrates=0
            ),
            'beer': CaloriesResponse(
                food_name='Beer',
                calories=43,
                serving_description='100 мл',
                protein=0.5,
                fat=0,
                carbohydrates=3.6
            ),
        }
        return mock_data.get(food_name)

    def search_food(self, food_name: str) -> Optional[Dict[str, Any]]:
        food_name = food_name.lower()
        print(f"Searching food: {food_name}")
        mock_data = {
            'chicken': {
                'food_name': 'Chicken',
                'calories': 150,
                'serving_description': '100 г',
                'protein': 30,
                'fat': 3.0,
                'carbohydrates': 0
            },
            'beer': {
                'food_name': 'Beer',
                'calories': 43,
                'serving_description': '100 мл',
                'protein': 0.5,
                'fat': 0,
                'carbohydrates': 3.6
            },
        }
        return mock_data.get(food_name)
