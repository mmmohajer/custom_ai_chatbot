from fastapi import FastAPI

from app.aibot.router import router as aibot_router

app = FastAPI()

app.include_router(aibot_router, prefix="/aibot", tags=["AI Bot"])


@app.get("/")
def root():
    return {"message": "API is running"}