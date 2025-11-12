from pydantic_settings import BaseSettings

class DefaultSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_URL: str
    SECRET_TOKEN: str

    # FatSecret API OAuth2 credentials
    FATSECRET_CONSUMER_KEY: str  # client id
    FATSECRET_CONSUMER_SECRET: str  # client secret

    class Config:
        env_file = ".env"

settings = None

def get_settings() -> DefaultSettings:
    global settings
    if settings is None:
        settings = DefaultSettings()
    return settings

