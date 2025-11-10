from pydantic_settings import BaseSettings

class DefaultSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_URL: str
    SECRET_TOKEN: str

    class Config:
        env_file = ".env"

settings = None

def get_settings() -> DefaultSettings:
    global settings
    if settings is None:
        settings = DefaultSettings()
    return settings

