from fastapi import APIRouter

from src.schemas import BodyTransaction
from src.schemas import ResponseTransactionMethod
from src.worker import WorkerTransaction
from config import logger

router = APIRouter(prefix="")

@router.post(
    "/create/transaction", description="Sends and saves a message about the creation of a transaction",
    response_model=ResponseTransactionMethod, tags=["TRANSACTION"]
)
async def create_transaction(body: BodyTransaction):
    """Creating a transaction, the default transaction status is 0"""
    try:
        return ResponseTransactionMethod(
            message=(await WorkerTransaction.create_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseTransactionMethod(message=False)

@router.put(
    "/create/transaction", description="Update a message about the creation of a transaction",
    response_model=ResponseTransactionMethod, tags=["TRANSACTION"]
)
async def update_transaction(body: BodyTransaction):
    """Updating the created transaction, the status is 1 or 3 if an error occurred."""
    try:
        return ResponseTransactionMethod(
            message=(await WorkerTransaction.update_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseTransactionMethod(message=False)

@router.post(
    "/send/transaction", description="Sends and saves a message about the sending of a transaction",
    response_model=ResponseTransactionMethod, tags=["TRANSACTION"]
)
async def send_transaction(body: BodyTransaction):
    """Sending a transaction, the status is 2"""
    try:
        return ResponseTransactionMethod(
            message=(await WorkerTransaction.send_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseTransactionMethod(message=False)