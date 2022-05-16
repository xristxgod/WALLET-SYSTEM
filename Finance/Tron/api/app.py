from fastapi import FastAPI

from config import Config
from src.services import endpoints, system

app = FastAPI(
    title=f"TronNetwork '{Config.NETWORK}'",
    description="Service for interacting with the Tron network.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(endpoints.router)
app.include_router(system.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app")
