from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pika import URLParameters, BlockingConnection

from src.__init__ import message_repository
from src.auth.auth_handler import JWTBearer
from src.schemas import ResponseStatus, ResponseMessageRepository
from src.endpoints.__init__ import router
from config import Config, logger

app = FastAPI(
    title=f"BotAlert",
    description="Service for interacting with the Bot alert!",
    version="1.0.0",
    dependencies=[Depends(JWTBearer())]
)
app.include_router(router)

@app.get("/", description="Find out the status of the API", response_model=ResponseStatus, tags=["SYSTEM"])
async def get_api_status():
    return ResponseStatus(message=True)

@app.get("/api/health/check/sender", description="Find out the status of the API",  response_model=ResponseStatus, tags=["SYSTEM"])
async def get_sender_status():
    connection: Optional[BlockingConnection] = None
    try:
        connection = BlockingConnection(URLParameters(url=Config.RABBITMQ_URL))
        channel = connection.channel()
        queue = channel.queue_declare(
            queue=Config.RABBITMQ_QUEUE_FOR_SENDER, durable=True,
            exclusive=False, auto_delete=False
        )
        return ResponseStatus(message=queue.method.message_count < 10)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return JSONResponse(content={"message": False})
    finally:
        if connection is not None:
            connection.close()

@app.get("/api/health/check/balancer", description="Find out the status of the API", response_model=ResponseStatus, tags=["SYSTEM"])
async def get_balancer_status():
    connection: Optional[BlockingConnection] = None
    try:
        connection = BlockingConnection(URLParameters(url=Config.RABBITMQ_URL))
        channel = connection.channel()
        queue = channel.queue_declare(
            queue=Config.RABBITMQ_QUEUE_FOR_BALANCER, durable=True,
            exclusive=False, auto_delete=False
        )
        return ResponseStatus(message=queue.method.message_count < 10)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return JSONResponse(content={"message": False})
    finally:
        if connection is not None:
            connection.close()

@app.get("/api/check/messages/cache", description="", response_model=ResponseMessageRepository, tags=["SYSTEM"])
async def get_message_repository_cache():
    cache = message_repository.messages
    try:
        return ResponseMessageRepository(
            repositoryCacheCount=len(cache),
            repositoryCacheData=cache,
            message=len(cache) < 15
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseMessageRepository(message=False)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app")