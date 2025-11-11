from typing import Dict, Any
from uuid import UUID
from app.service import MainService

service = MainService()


def process_text(model: Dict[str, Any]) -> str:
    raw = (model.get("raw_text") or "").strip()
    user_id = model.get("user", {}).get("id")
    who = f" (user_id={user_id})" if user_id is not None else ""
    return f"Ты написал{who}: {raw}"


async def start(model: Dict[str, Any]) -> str:
    user_id = UUID(model.get("user", {}).get("id"))
    chat_id = UUID(model.get("chat", {}).get("id", str(user_id)))
    await service.start_user(user_id, chat_id)
    return "Бот запущен! Используй команды для работы."


async def product_count_manual(model: Dict[str, Any]) -> str:
    user_id = UUID(model.get("user", {}).get("id"))
    product_name = model.get("product_name", "")
    calories = model.get("calories", 0)

    result = await service.product_count_manual(user_id, product_name, calories)
    if result is None:
        return "Продукт не найден"

    return f"Можешь съесть {result:.1f}г {product_name}"


async def product_count(model: Dict[str, Any]) -> str:
    user_id = UUID(model.get("user", {}).get("id"))
    days = model.get("days")

    result = await service.product_count(user_id, days)
    if result is None:
        return "Не удалось рассчитать"

    days_str = f" за {days} дней" if days else ""
    return f"Можешь съесть {result:.1f}г{days_str}"


async def change_product(model: Dict[str, Any]) -> str:
    user_id = UUID(model.get("user", {}).get("id"))
    product_name = model.get("product_name", "")

    result = await service.change_product(user_id, product_name)
    if not result:
        return "Продукт не найден"

    return f"Продукт изменён на {product_name}"


async def add_custom_product(model: Dict[str, Any]) -> str:
    user_id = UUID(model.get("user", {}).get("id"))
    product_name = model.get("product_name", "")
    calories = model.get("calories", 0)

    result = await service.add_custom_product(user_id, product_name, calories)
    if not result:
        return "Продукт уже существует"

    return f"Продукт {product_name} добавлен"


async def notify(model: Dict[str, Any]) -> str:
    return "Уведомления появятся позже"


async def get_product(model: Dict[str, Any]) -> str:
    user_id = UUID(model.get("user", {}).get("id"))

    result = await service.get_product(user_id)
    if result is None:
        return "Продукт не найден"

    return f"Текущий продукт: {result}"
