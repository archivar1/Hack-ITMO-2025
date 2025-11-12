from pydantic import BaseModel


class CaloriesRequest(BaseModel):
    food_name: str


class CaloriesResponse(BaseModel):
    food_name: str
    calories: float
    serving_description: str
    protein: float
    fat: float
    carbohydrates: float
