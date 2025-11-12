import logging
from typing import Final

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
from app.service import process_text

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("tg-bot")


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Привет! Я бот, которому нужно придумать речевку"
    )
    await update.message.reply_text(text)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Доступно:\n"
        "• просто напиши текст — я отвечу тем, что «вернула логика».\n"
        "• /start — приветствие\n"
        "• /help — эта помощь\n"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    incoming = update.message.text
    user_id = update.effective_user.id if update.effective_user else None

    try:
        reply = process_text(incoming, user_id)
    except Exception as e:
        log.exception("Ошибка в бизнес-логике: %s", e)
        reply = "Упс, что-то пошло не так. Попробуй ещё раз."

    await update.message.reply_text(reply)

def build_app(token: str) -> Application:
    app = (
        ApplicationBuilder()
        .token(token)
        .build()
    )

    # TODO добавить все команды
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    # Текстовые сообщения (всё, что не команда)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    return app

def main() -> None:
    token = get_settings().TELEGRAM_BOT_TOKEN
    app = build_app(token)
    app.run_polling(allowed_updates=Update.ALL_TYPES, stop_signals=None)

if __name__ == "__main__":
    main()