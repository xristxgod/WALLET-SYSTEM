from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.endpoints.__init__ import router

app = FastAPI(
    title=f"BotAlert",
    description="Service for interacting with the Tron network.",
    version="1.0.0",
    docs_url="/bot/docs",
    redoc_url="/bot/redoc",
)
app.include_router(router)

@app.get("/", description="Find out the status of the API", response_class=JSONResponse, tags=["System"])
async def get_api_status():
    return JSONResponse(content={"message": True})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app")