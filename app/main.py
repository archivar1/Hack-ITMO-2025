from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
import threading
import logging
from telegram import Update
from app.fatsecret_service import FatSecretService
from app.models import CaloriesResponse, CaloriesRequest
from app.bot import build_app
from app.config import get_settings

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("main")

bot_thread = None


def run_bot():
    bot_logger = logging.getLogger("tg-bot")
    try:
        bot_logger.info("=" * 50)
        bot_logger.info("Запуск Telegram бота...")
        token = get_settings().TELEGRAM_BOT_TOKEN
        if not token:
            error_msg = "TELEGRAM_BOT_TOKEN не задан в .env"
            bot_logger.error(error_msg)
            raise RuntimeError(error_msg)
        bot_logger.info("Токен бота получен, инициализация приложения...")
        bot_app = build_app(token)
        bot_logger.info("Бот успешно инициализирован, запуск polling...")
        bot_logger.info("=" * 50)
        bot_app.run_polling(allowed_updates=Update.ALL_TYPES, stop_signals=None)
    except Exception as e:
        bot_logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global bot_thread
    logger.info("=" * 50)
    logger.info("Запуск приложения: FastAPI + Telegram Bot")
    logger.info("Создание потока для Telegram бота...")
    bot_thread = threading.Thread(target=run_bot, daemon=True, name="TelegramBot")
    bot_thread.start()
    logger.info(f"Поток бота запущен: {bot_thread.name} (ID: {bot_thread.ident})")
    logger.info("FastAPI сервер готов к работе")
    logger.info("=" * 50)
    yield
    # Shutdown
    logger.info("Завершение работы приложения...")


app = FastAPI(lifespan=lifespan)

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
    logger.info("Запуск FastAPI сервера на http://0.0.0.0:8000")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    main()