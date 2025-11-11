from fastapi import FastAPI
from pydantic import BaseModel
from app.config.config import DefaultSettings, get_settings
from uvicorn import run
from app.endpoints import list_of_routes

def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    description = ""

    application = FastAPI(
        docs_url="/api/v1/swagger",
        openapi_url="/api/v1/openapi",
        version="1.0.0",
        title="MasterProject",
        description=description,
    )

    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

settings = get_settings()


if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "main:app",
        port=settings_for_application.BACKEND_PORT,
        reload=True,
        reload_dirs=["app"],
        log_level="debug",
        host=settings_for_application.BACKEND_HOST,
    )
