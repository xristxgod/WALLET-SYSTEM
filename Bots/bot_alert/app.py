from fastapi import FastAPI

from src.endpoints import router

app = FastAPI(
    title=f"BotAlert",
    description="Service for interacting with the Tron network.",
    version="1.0.0",
    docs_url="/bot/docs",
    redoc_url="/bot/redoc"
)
app.include_router(router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app")