from pydantic import BaseModel
from app.config.config import DefaultSettings, get_settings
from uvicorn import run


settings = get_settings()


if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "main:app",
        port=settings_for_application.BACKEND_PORT,
        reload=False,
        reload_dirs=["app"],
        log_level="debug",
        host=settings_for_application.BACKEND_HOST,
    )
