from typing import Optional


class HumanApiServiceMock:
    def get_calories_burned(self, product_name: str, days: int = 1) -> Optional[int]:
        if product_name.lower() == 'chicken':
            return 100 * days
        return None
