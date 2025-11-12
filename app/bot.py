import logging
from typing import Optional, Dict, Any

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.config import get_settings
from app import service as svc


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("tg-bot")


# ====================== УТИЛИТЫ ======================
def _user_id(update: Update) -> Optional[int]:
    return update.effective_user.id if update.effective_user else None

def _user_meta(update: Update) -> Dict[str, Any]:
    u = update.effective_user
    return {
        "id": u.id if u else None,
        "is_bot": u.is_bot if u else None,
        "username": getattr(u, "username", None),
        "first_name": getattr(u, "first_name", None),
        "last_name": getattr(u, "last_name", None),
        "language_code": getattr(u, "language_code", None),
    }

def _chat_meta(update: Update) -> Dict[str, Any]:
    c = update.effective_chat
    return {
        "id": c.id if c else None,
        "type": getattr(c, "type", None),
        "title": getattr(c, "title", None),
        "username": getattr(c, "username", None),
    }

def _extract_args_text(text: str, command: str) -> str:
    if not text:
        return ""
    variants = [
        f"/{command} ",
        f"/{command}@",
    ]
    for p in variants:
        if text.startswith(p):
            if p.endswith("@"):
                space_pos = text.find(" ")
                return text[space_pos + 1 :] if space_pos != -1 else ""
            return text[len(p):]
    return ""

def _build_full_model(update: Update, command: str) -> Dict[str, Any]:
    msg = update.effective_message
    return {
        "command": command,
        "raw_text": (msg.text or "") if msg else "",
        "args_text": _extract_args_text(msg.text or "", command) if msg and command != "text" else "",
        "entities": [e.to_dict() for e in (msg.entities or [])] if msg else [],
        "user": _user_meta(update),
        "chat": _chat_meta(update),
        "date": msg.date.isoformat() if msg and msg.date else None,
        "message_id": msg.message_id if msg else None,
    }


# ====================== ОБРАБОТЧИКИ ======================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот. Команды: /help")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Доступные команды:\n"
        "/start — начало работы\n"
        "/help — помощь\n"
        "/connect_human — подключить Human API для получения данных о здоровье\n"
        "/product_count_manual — подсчёт калорий вручную (сырые данные пойдут в сервис)\n"
        "/product_count — подсчёт по HumanAPI\n"
        "/change_product — сменить текущий продукт\n"
        "/add_custom_product — добавить персональный продукт\n"
        "/notify — авто-оповещение за прошлый день\n"
        "/get_product — показать текущий продукт\n"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def _call_service_and_reply(update: Update, command: str, handler):
    model = _build_full_model(update, command)
    try:
        reply = handler(model)
    except Exception as e:
        log.exception("Service handler failed for %s: %s", command, e)
        reply = f"Заглушка: /{command} — реализация появится позже."
    await update.message.reply_text(reply)


# ====== Команды ======
async def connect_human_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "connect_human", svc.connect_human_api)

async def product_count_manual_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "product_count_manual", svc.product_count_manual)

async def product_count_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "product_count", svc.product_count)

async def change_product_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "change_product", svc.change_product)

async def add_custom_product_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "add_custom_product", svc.add_custom_product)

async def notify_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "notify", svc.notify)

async def get_product_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _call_service_and_reply(update, "get_product", svc.get_product)


# ====== Текст ======
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model = _build_full_model(update, "text")
    reply = svc.process_text(model)
    await update.message.reply_text(reply)


def build_app(token: str) -> Application:
    app = ApplicationBuilder().token(token).build()

    # Базовые команды
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    # Команды только с подчёркиванием
    app.add_handler(CommandHandler("connect_human", connect_human_cmd))
    app.add_handler(CommandHandler("product_count_manual", product_count_manual_cmd))
    app.add_handler(CommandHandler("product_count", product_count_cmd))
    app.add_handler(CommandHandler("change_product", change_product_cmd))
    app.add_handler(CommandHandler("add_custom_product", add_custom_product_cmd))
    app.add_handler(CommandHandler("notify", notify_cmd))
    app.add_handler(CommandHandler("get_product", get_product_cmd))

    # Обычный текст
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    return app


def main() -> None:
    token = get_settings().TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан в .env")
    app = build_app(token)
    app.run_polling(allowed_updates=Update.ALL_TYPES, stop_signals=None)


if __name__ == "__main__":
    main()
