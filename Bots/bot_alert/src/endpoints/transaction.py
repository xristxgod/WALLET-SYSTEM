from fastapi import APIRouter

router = APIRouter(prefix="/transaction")

@router.post("/create")
async def create_transaction():
    pass

@router.post("/send")
async def send_transaction():
    pass