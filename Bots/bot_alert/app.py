from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pika import URLParameters, BlockingConnection

from src.endpoints.__init__ import router
from config import Config, logger

app = FastAPI(
    title=f"BotAlert",
    description="Service for interacting with the Bot alert!",
    version="1.0.0",
)
app.include_router(router)

@app.get("/", description="Find out the status of the API", response_class=JSONResponse, tags=["SYSTEM"])
async def get_api_status():
    return JSONResponse(content={"message": True})

@app.get("/api/health/check/sender", description="Find out the status of the API", response_class=JSONResponse, tags=["SYSTEM"])
async def get_sender_status():
    connection: Optional[BlockingConnection] = None
    try:
        connection = BlockingConnection(URLParameters(url=Config.RABBITMQ_URL))
        channel = connection.channel()
        queue = channel.queue_declare(
            queue=Config.RABBITMQ_QUEUE_FOR_SENDER, durable=True,
            exclusive=False, auto_delete=False
        )
        return JSONResponse(content={"message": queue.method.message_count < 10})
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return JSONResponse(content={"message": False})
    finally:
        if connection is not None:
            connection.close()

@app.get("/api/health/check/balancer", description="Find out the status of the API", response_class=JSONResponse, tags=["SYSTEM"])
async def get_sender_status():
    connection: Optional[BlockingConnection] = None
    try:
        connection = BlockingConnection(URLParameters(url=Config.RABBITMQ_URL))
        channel = connection.channel()
        queue = channel.queue_declare(
            queue=Config.RABBITMQ_QUEUE_FOR_BALANCER, durable=True,
            exclusive=False, auto_delete=False
        )
        return JSONResponse(content={"message": queue.method.message_count < 10})
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return JSONResponse(content={"message": False})
    finally:
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app")