from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from app.fatsecret_service import FatSecretService
from app.models import CaloriesResponse, CaloriesRequest

app = FastAPI()

fatsecret_service = FatSecretService()


@app.get("/")
async def root():
    return {"message": "Telegram Bot API is running!", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/calories", response_model=CaloriesResponse)
async def get_calories(food_name: str = Query(...)):
    """
    Получить КБЖУ блюда по названию (GET запрос).
    
    Для блюд из нескольких слов пробелы можно заменить на %20 или +
    
    Args:
        food_name
    
    Returns:
        CaloriesResponse: КБЖУ блюда на 100 г/мл
    """
    try:
        result = fatsecret_service.get_calories(food_name)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Блюдо '{food_name}' не найдено"
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении информации о блюде: {str(e)}"
        )


@app.post("/calories", response_model=CaloriesResponse)
async def get_calories_post(request: CaloriesRequest):
    """
    Получить КБЖУ блюда по названию (POST запрос).
    
    Args:
        food_name
    
    Returns:
        CaloriesResponse: КБЖУ блюда на 100 г/мл
    """

    try:
        result = fatsecret_service.get_calories(request.food_name)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Блюдо '{request.food_name}' не найдено"
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении информации о блюде: {str(e)}"
        )


def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    main()