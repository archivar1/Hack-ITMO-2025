from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_URL: str
    SECRET_TOKEN: str

    # FatSecret API OAuth2 credentials
    FATSECRET_CONSUMER_KEY: str  # client id
    FATSECRET_CONSUMER_SECRET: str  # client secret

    # Human API credentials
    HUMAN_API_CLIENT_ID: str
    HUMAN_API_CLIENT_SECRET: str
    HUMAN_API_REDIRECT_URI: str

    class Config:
        env_file = ".env"

settings = None

def get_settings() -> DefaultSettings:
    global settings
    if settings is None:
        settings = DefaultSettings()
    return settings

