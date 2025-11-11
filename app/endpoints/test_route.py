from fastapi import APIRouter

api_router = APIRouter(prefix="/test", tags=["Test"])


@api_router.get("/")
async def root():
    return {"message": "Telegram Bot API is running!", "status": "healthy"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}