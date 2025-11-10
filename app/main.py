from fastapi import FastAPI, HTTPException, Header, Request, Depends
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Telegram Bot API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}



def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    main()