from typing import Optional


class HumanApiServiceMock:
    def get_calories_burned(self, days: Optional[int] = 1) -> int:
        return 100 * (days if days else 1)
