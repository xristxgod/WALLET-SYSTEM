from fastapi import APIRouter

router = APIRouter(prefix="/checker")

@router.post("/bad")
async def create_transaction():
    pass

@router.post("/good")
async def create_transaction():
    pass