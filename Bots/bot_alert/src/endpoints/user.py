from fastapi import APIRouter
from src.schemas import BodyRegUser, BodyBalance, BodyInfo
from src.schemas import ResponseUserMethod

from src.worker import WorkerUser
from config import logger

router = APIRouter(prefix="/user")

@router.post(
    "/reg", description="Sends a message to the notification bot that a new user has appeared",
    response_model=ResponseUserMethod, tags=["USER"]
)
async def reg_user(body: BodyRegUser):
    try:
        return ResponseUserMethod(
            message=(await WorkerUser.reg_user_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseUserMethod(message=False)

@router.post(
    "/add", description="Sends a message to the notification bot about what happened to the deposit balance!",
    response_model=ResponseUserMethod, tags=["USER"]
)
async def add_balance(body: BodyBalance):
    try:
        return ResponseUserMethod(
            message=(await WorkerUser.balance_text(body=body, is_add=True))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseUserMethod(message=False)

@router.post(
    "/dec", description="Sends a message to the notifier bot about what happened the balance debit!",
    response_model=ResponseUserMethod, tags=["USER"]
)
async def add_balance(body: BodyBalance):
    try:
        return ResponseUserMethod(
            message=(await WorkerUser.balance_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseUserMethod(message=False)

@router.post(
    "/info", description="This router sends a message with information!",
    response_model=ResponseUserMethod, tags=["USER"]
)
async def info_message(body: BodyInfo):
    try:
        return ResponseUserMethod(
            message=(await WorkerUser.info_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseUserMethod(message=False)