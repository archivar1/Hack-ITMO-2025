from typing import Dict, Any
from uuid import UUID
from app.service import MainService

service = MainService()


def process_text(model: Dict[str, Any]) -> str:
    raw = (model.get("raw_text") or "").strip()
    chat_id = model.get("chat", {}).get("id")
    who = f" (chat_id={chat_id})" if chat_id is not None else ""
    return f"Ты написал{who}: {raw}"


async def start(model: Dict[str, Any]) -> str:
    chat_id = model.get("chat", {}).get("id")
    if chat_id is None:
        return "Ошибка: не удалось определить пользователя"

    await service.start_user(chat_id)
    return "Бот запущен! Используй команды для работы."


async def product_count_manual(model: Dict[str, Any]) -> str:
    chat_id = model.get("chat", {}).get("id")
    if chat_id is None:
        return "Ошибка: не удалось определить пользователя"

    args_text = model.get("args_text", "").strip()
    if not args_text:
        return "Использование: /product_count_manual <название продукта> <калории>\nНапример: /product_count_manual яблоко 100"

    parts = args_text.rsplit(maxsplit=1)
    if len(parts) < 2:
        return "Использование: /product_count_manual <название продукта> <калории>\nНапример: /product_count_manual яблоко 100"

    product_name = parts[0].strip()
    try:
        calories = int(parts[1])
    except ValueError:
        return "Ошибка: калории должны быть числом"

    user_id = await service.get_or_create_user_by_chat_id(chat_id)
    result = await service.product_count_manual(user_id, product_name, calories)
    if result is None:
        return "Продукт не найден"

    return f"Можешь съесть {result:.1f}г {product_name}"


async def product_count(model: Dict[str, Any]) -> str:
    chat_id = model.get("chat", {}).get("id")
    if chat_id is None:
        return "Ошибка: не удалось определить пользователя"

    user_id = await service.get_or_create_user_by_chat_id(chat_id)
    days = model.get("days")

    result = await service.product_count(user_id, days)
    if result is None:
        return "Не удалось рассчитать"

    amount = result["amount"]
    product_name = result["product_name"]
    days_str = f" за {days} дней" if days else ""
    return f"Можешь съесть {amount:.1f}г {product_name}{days_str}"


async def change_product(model: Dict[str, Any]) -> str:
    chat_id = model.get("chat", {}).get("id")
    if chat_id is None:
        return "Ошибка: не удалось определить пользователя"

    args_text = model.get("args_text", "").strip()
    if not args_text:
        return "Использование: /change_product <название продукта>\nНапример: /change_product яблоко"

    product_name = args_text
    user_id = await service.get_or_create_user_by_chat_id(chat_id)
    result = await service.change_product(user_id, product_name)
    if not result:
        return "Продукт не найден"

    return f"Продукт изменён на {product_name}"


async def add_custom_product(model: Dict[str, Any]) -> str:
    chat_id = model.get("chat", {}).get("id")
    if chat_id is None:
        return "Ошибка: не удалось определить пользователя"

    args_text = model.get("args_text", "").strip()
    if not args_text:
        return "Использование: /add_custom_product <название продукта> <калории>\nНапример: /add_custom_product яблоко 52"

    parts = args_text.rsplit(maxsplit=1)
    if len(parts) < 2:
        return "Использование: /add_custom_product <название продукта> <калории>\nНапример: /add_custom_product яблоко 52"

    product_name = parts[0].strip()
    try:
        calories = int(parts[1])
    except ValueError:
        return "Ошибка: калории должны быть числом"

    user_id = await service.get_or_create_user_by_chat_id(chat_id)
    result = await service.add_custom_product(user_id, product_name, calories)
    if not result:
        return "Продукт уже существует"

    return f"Продукт {product_name} добавлен"


async def notify(model: Dict[str, Any]) -> str:
    return "Уведомления появятся позже"


async def get_product(model: Dict[str, Any]) -> str:
    chat_id = model.get("chat", {}).get("id")
    if chat_id is None:
        return "Ошибка: не удалось определить пользователя"

    user_id = await service.get_or_create_user_by_chat_id(chat_id)

    result = await service.get_product(user_id)
    if result is None:
        return "Продукт не найден"

    return f"Текущий продукт: {result['name']} ({result['calories']} ккал/100г)"
