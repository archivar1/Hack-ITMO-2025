from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from typing import Optional, Dict, Any
from datetime import datetime
from app.fatsecret_service import FatSecretService
from app.human_api_service import HumanAPIService
from app.models import (
    CaloriesResponse, CaloriesRequest,
    HumanAPIAuthResponse, HumanAPITokenResponse,
    StepsResponse, CaloriesBurnedResponse, ActivitiesResponse
)

app = FastAPI()

fatsecret_service = FatSecretService()
human_api_service = HumanAPIService()

# {user_id: {"access_token": "...", "refresh_token": "...", "expires_at": ...}}
user_tokens: Dict[str, Dict[str, Any]] = {}


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


@app.get("/auth/human/connect", response_model=HumanAPIAuthResponse)
async def connect_human_api(user_id: str = Query(..., description="ID пользователя")):
    """
    Получить URL для авторизации пользователя в Human API.

    Пользователь должен перейти по этому URL, авторизоваться и разрешить доступ к данным.
    """
    try:
        auth_url = human_api_service.get_authorization_url(user_id, state=user_id)
        return HumanAPIAuthResponse(
            authorization_url=auth_url,
            state=user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании URL авторизации: {str(e)}"
        )


@app.get("/auth/human/callback")
async def human_api_callback(
    code: str = Query(..., description="Authorization code от Human API"),
    state: str = Query(..., description="State параметр (user_id)")
):
    """
    Callback endpoint для обработки ответа от Human API после авторизации.

    Обменивает authorization code на session token и сохраняет его.
    """
    try:
        token_data = human_api_service.exchange_code_for_token(code)

        user_tokens[state] = {
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": datetime.now().timestamp() + token_data.get("expires_in", 3600)
        }

        return {
            "status": "success",
            "message": "Авторизация успешна. Токен сохранен.",
            "user_id": state
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обмене кода на токен: {str(e)}"
        )


@app.get("/api/human/steps", response_model=StepsResponse)
async def get_steps(
    user_id: str = Query(..., description="ID пользователя"),
    date: Optional[str] = Query(None, description="Дата в формате YYYY-MM-DD или 'today'")
):
    """
    Получить количество шагов пользователя за указанную дату.
    """
    if user_id not in user_tokens:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не авторизован в Human API. Используйте /auth/human/connect"
        )

    session_token = user_tokens[user_id]["access_token"]

    try:
        date_str = date or "today"
        if date_str == "today":
            date_str = datetime.now().strftime('%Y-%m-%d')

        data = human_api_service.get_steps(session_token, date_str)

        if data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Данные о шагах за {date_str} не найдены"
            )

        return StepsResponse(
            date=date_str,
            steps=data.get("steps"),
            distance=data.get("distance"),
            calories=data.get("calories")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении данных о шагах: {str(e)}"
        )


@app.get("/api/human/calories", response_model=CaloriesBurnedResponse)
async def get_calories_burned(
    user_id: str = Query(..., description="ID пользователя"),
    date: Optional[str] = Query(None, description="Дата в формате YYYY-MM-DD или 'today'")
):
    """
    Получить количество сожженных калорий пользователя за указанную дату.
    """
    if user_id not in user_tokens:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не авторизован в Human API. Используйте /auth/human/connect"
        )

    session_token = user_tokens[user_id]["access_token"]

    try:
        date_str = date or "today"
        if date_str == "today":
            date_str = datetime.now().strftime('%Y-%m-%d')

        calories = human_api_service.get_calories(session_token, date_str)

        if calories is None:
            raise HTTPException(
                status_code=404,
                detail=f"Данные о калориях за {date_str} не найдены"
            )

        activities = human_api_service.get_activities(session_token, date_str)

        return CaloriesBurnedResponse(
            date=date_str,
            calories=calories,
            activities_count=len(activities) if activities else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении данных о калориях: {str(e)}"
        )


@app.get("/api/human/activities", response_model=ActivitiesResponse)
async def get_activities(
    user_id: str = Query(..., description="ID пользователя"),
    date: Optional[str] = Query(None, description="Дата в формате YYYY-MM-DD или 'today'")
):
    """
    Получить список активностей пользователя за указанную дату.
    """
    if user_id not in user_tokens:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не авторизован в Human API. Используйте /auth/human/connect"
        )

    session_token = user_tokens[user_id]["access_token"]

    try:
        date_str = date or "today"
        if date_str == "today":
            date_str = datetime.now().strftime('%Y-%m-%d')

        activities = human_api_service.get_activities(session_token, date_str)

        from app.models import ActivityResponse
        activity_responses = [ActivityResponse(**act) for act in activities]

        total_calories = sum(act.get("calories", 0) for act in activities if act.get("calories"))

        return ActivitiesResponse(
            date=date_str,
            activities=activity_responses,
            total_calories=total_calories if total_calories > 0 else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении данных об активностях: {str(e)}"
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