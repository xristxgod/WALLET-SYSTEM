from fastapi import APIRouter

from src.schemas import BodyTransaction
from src.schemas import ResponseTransactionMethod
from src.worker import WorkerTransaction
from config import logger

router = APIRouter(prefix="/transaction")

@router.post(
    "/create", description="Sends and saves a message about the creation of a transaction",
    response_model=ResponseTransactionMethod, tags=["TRANSACTION"]
)
async def create_transaction(body: BodyTransaction):
    try:
        return ResponseTransactionMethod(
            message=(await WorkerTransaction.create_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseTransactionMethod(message=False)

@router.post("/send")
async def send_transaction():
    pass