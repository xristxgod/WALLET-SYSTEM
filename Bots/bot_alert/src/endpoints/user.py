from fastapi import APIRouter
from src.schemas import BodyRegUser, ResponseUserMethod

router = APIRouter(prefix="/user")

@router.post(
    "/reg", description="Sends a message to the notification bot that a new user has appeared",
    response_model=ResponseUserMethod, tags=["USER"]
)
def reg_user(body: BodyRegUser):
    pass

@router.post("/add")
def add_balance(body):
    pass

@router.post("/dec")
def add_balance(body):
    pass