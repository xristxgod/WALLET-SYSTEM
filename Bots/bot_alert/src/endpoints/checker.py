from fastapi import APIRouter

from src.schemas import BodyNews, BodyInfoChecker
from src.schemas import ResponseCheckerMethod

from src.worker import WorkerChecker

from config import logger

router = APIRouter(prefix="/checker")

@router.post(
    "/bad", description="Notifies admins about bad news",
    response_model=ResponseCheckerMethod, tags=["CHECKER"]
)
async def bad_news(body: BodyNews):
    try:
        return ResponseCheckerMethod(
            message=(await WorkerChecker.news_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseCheckerMethod(message=False)

@router.post(
    "/good", description="Notifies admins about good news",
    response_model=ResponseCheckerMethod, tags=["CHECKER"]
)
async def good_news(body: BodyNews):
    try:
        return ResponseCheckerMethod(
            message=(await WorkerChecker.news_text(body=body, is_good=True))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseCheckerMethod(message=False)

@router.post(
    "/info", description="Notifies about some information",
    response_model=ResponseCheckerMethod, tags=["CHECKER"]
)
async def info(body: BodyInfoChecker):
    try:
        return ResponseCheckerMethod(
            message=(await WorkerChecker.info_text(body=body))
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseCheckerMethod(message=False)