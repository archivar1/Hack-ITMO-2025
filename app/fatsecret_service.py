import requests
from typing import Optional, Dict, Any
from app.config import get_settings
from app.models import CaloriesResponse


class FatSecretService:
    BASE_URL = "https://platform.fatsecret.com/rest/server.api"
    TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

    def __init__(self):
        settings = get_settings()
        self.client_id = settings.FATSECRET_CONSUMER_KEY
        self.client_secret = settings.FATSECRET_CONSUMER_SECRET
        self._access_token = None

    def _get_access_token(self) -> str:
        if self._access_token:
            return self._access_token

        try:
            response = requests.post(
                self.TOKEN_URL,
                data={
                    'grant_type': 'client_credentials',
                    'scope': 'basic'
                },
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            token_data = response.json()
            self._access_token = token_data['access_token']
            return self._access_token
        except requests.exceptions.RequestException as e:
            error_detail = f"{str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_detail += f" | Response: {error_data}"
                except:
                    error_detail += f" | Status: {e.response.status_code} | Text: {e.response.text[:200]}"
            raise Exception(f"Ошибка при получении токена доступа: {error_detail}")

    def search_food(self, food_name: str) -> Optional[Dict[str, Any]]:
        params = {
            'method': 'foods.search',
            'search_expression': food_name,
            'format': 'json',
            'max_results': 1
        }

        try:
            access_token = self._get_access_token()
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(self.BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                error_msg = data['error'].get('message', 'Unknown error')
                raise Exception(f"FatSecret API error: {error_msg}")

            if 'foods' in data and 'food' in data['foods']:
                foods = data['foods']['food']
                if isinstance(foods, list) and len(foods) > 0:
                    return foods[0]
                elif isinstance(foods, dict):
                    return foods
            return None
        except requests.exceptions.RequestException as e:
            error_detail = f"{str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_detail += f" | Response: {error_data}"
                except:
                    error_detail += f" | Status: {e.response.status_code} | Text: {e.response.text[:200]}"
            raise Exception(f"Ошибка при поиске продукта: {error_detail}")

    def get_food_details(self, food_id: str) -> Optional[Dict[str, Any]]:
        params = {
            'method': 'food.get',
            'food_id': food_id,
            'format': 'json'
        }

        try:
            access_token = self._get_access_token()
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(self.BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                error_msg = data['error'].get('message', 'Unknown error')
                raise Exception(f"FatSecret API error: {error_msg}")

            if 'food' in data:
                return data['food']
            return None
        except requests.exceptions.RequestException as e:
            error_detail = f"{str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_detail += f" | Response: {error_data}"
                except:
                    error_detail += f" | Status: {e.response.status_code} | Text: {e.response.text[:200]}"
            raise Exception(f"Ошибка при получении информации о продукте: {error_detail}")

    def get_calories(self, food_name: str) -> Optional[CaloriesResponse]:
        food = self.search_food(food_name)
        if not food:
            return None

        food_id = food.get('food_id')
        if not food_id:
            return None

        food_details = self.get_food_details(str(food_id))
        if not food_details:
            return None

        servings = food_details.get('servings', {})
        serving_list = servings.get('serving', [])

        if not serving_list:
            return None

        if not isinstance(serving_list, list):
            serving_list = [serving_list]

        serving_100g = None
        for serving in serving_list:
            try:
                metric_amount = float(serving.get('metric_serving_amount', 0))
                metric_unit = str(serving.get('metric_serving_unit', '')).lower()

                if metric_amount == 100.0 and metric_unit in ['g', 'ml', 'gram', 'milliliter']:
                    serving_100g = serving
                    break
            except (ValueError, TypeError):
                continue

        if not serving_100g:
            for serving in serving_list:
                try:
                    metric_amount = float(serving.get('metric_serving_amount', 0))
                    metric_unit = str(serving.get('metric_serving_unit', '')).lower()

                    if metric_amount > 0 and metric_unit in ['g', 'ml', 'gram', 'milliliter']:
                        serving_100g = serving
                        break
                except (ValueError, TypeError):
                    continue

        if serving_100g:
            try:
                metric_amount = float(serving_100g.get('metric_serving_amount', 1))
                metric_unit = str(serving_100g.get('metric_serving_unit', 'g')).lower()
            except (ValueError, TypeError):
                metric_amount = 1.0
                metric_unit = 'g'

            if metric_amount > 0:
                multiplier = 100.0 / metric_amount
            else:
                multiplier = 1.0

            if 'ml' in metric_unit or 'milliliter' in metric_unit:
                serving_desc = "100 мл"
            else:
                serving_desc = "100 г"

            return CaloriesResponse(
                food_name=food_details.get('food_name', food_name),
                calories=float(serving_100g.get('calories', 0)) * multiplier,
                serving_description=serving_desc,
                protein=float(serving_100g.get('protein', 0)) * multiplier,
                fat=float(serving_100g.get('fat', 0)) * multiplier,
                carbohydrates=float(serving_100g.get('carbohydrate', 0)) * multiplier,
            )

        serving = serving_list[0]
        return CaloriesResponse(
            food_name=food_details.get('food_name', food_name),
            calories=float(serving.get('calories', 0)),
            serving_description="100 г",
            protein=float(serving.get('protein', 0)),
            fat=float(serving.get('fat', 0)),
            carbohydrates=float(serving.get('carbohydrate', 0)),
        )
