from typing import Optional
from datetime import datetime


class HumanApiServiceMock:
    CALORIES_PER_DAY = 2100  # средние калории за полный день

    def get_calories_burned(self, days: Optional[int] = 1) -> int:
        if not days or days < 1:
            days = 1

        # Калории за прошлые дни
        total_calories = self.CALORIES_PER_DAY * (days - 1)

        # Калории за текущий день в зависимости от времени
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        time_in_hours = hour + minute / 60

        if time_in_hours < 7:
            progress = time_in_hours * 0.02
        elif time_in_hours < 22:
            progress = 0.14 + (time_in_hours - 7) * 0.055
        else:
            progress = 0.97

        today_calories = int(self.CALORIES_PER_DAY * progress)

        return total_calories + today_calories
