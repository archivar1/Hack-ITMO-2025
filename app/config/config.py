from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    TELEGRAM_BOT_TOKEN: str
    PATH_PREFIX: str
    BACKEND_HOST: str
    BACKEND_PORT: int
    WEBHOOK_URL: str
    SECRET_TOKEN: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    @property
    def database_settings(self) -> dict:

        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:

        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )


    @property
    def database_uri_sync(self) -> str:

        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

settings: DefaultSettings | None = None

def get_settings() -> DefaultSettings:
    global settings
    if settings is None:
        settings = DefaultSettings()
    return settings
