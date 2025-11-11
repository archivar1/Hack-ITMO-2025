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
