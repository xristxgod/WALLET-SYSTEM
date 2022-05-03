from fastapi import FastAPI

from config import Config
from src.services.endpoints import router

app = FastAPI(
    title=f"TronNetwork '{Config.NETWORK}'",
    description="Service for interacting with the Tron network.",
    version="1.0.0",
    docs_url="/tron/docs",
    redoc_url="/tron/redoc"
)
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app")