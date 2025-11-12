from typing import Dict, Any


# ====== ОБРАБОТКА СВОБОДНОГО ТЕКСТА ======
def process_text(model: Dict[str, Any]) -> str:
    raw = (model.get("raw_text") or "").strip()
    user_id = model.get("user", {}).get("id")
    who = f" (user_id={user_id})" if user_id is not None else ""
    return f"Ты написал{who}: {raw}"


# ====== ЗАГЛУШКИ ДЛЯ КОМАНД ======
def product_count_manual(model: Dict[str, Any]) -> str:
    return "Заглушка: /product_count_manual — реализация появится позже."

def connect_human_api(model: Dict[str, Any]) -> str:
    """
    Подключить Human API для получения данных о здоровье.
    """
    user_id = model.get("user", {}).get("id")
    if not user_id:
        return "Ошибка: не удалось определить ID пользователя."

    try:
        from app.config import get_settings
        settings = get_settings()

        user_id_str = str(user_id)
        base_url = getattr(settings, 'WEBHOOK_URL', 'http://localhost:8000').rstrip('/')
        auth_url = f"{base_url}/auth/human/connect?user_id={user_id_str}"

        return (
            "🔗 Подключение Human API\n\n"
            "Для подключения:\n"
            "1. Перейдите по ссылке ниже\n"
            "2. Войдите в Human API\n"
            "3. Выберите источники данных (HealthKit, Google Fit и т.д.)\n"
            "4. Разрешите доступ к данным о здоровье\n"
            "5. После авторизации используйте /product_count для получения данных\n\n"
            f"Ссылка: {auth_url}"
        )
    except Exception as e:
        return f"Ошибка при создании ссылки: {str(e)}"


def product_count(model: Dict[str, Any]) -> str:
    return "Заглушка: /product_count — реализация появится позже."

def change_product(model: Dict[str, Any]) -> str:
    return "Заглушка: /change_product — реализация появится позже."

def add_custom_product(model: Dict[str, Any]) -> str:
    return "Заглушка: /add_custom_product — реализация появится позже."

def notify(model: Dict[str, Any]) -> str:
    return "Заглушка: /notify — реализация появится позже."

def get_product(model: Dict[str, Any]) -> str:
    return "Заглушка: /get_product — реализация появится позже."
