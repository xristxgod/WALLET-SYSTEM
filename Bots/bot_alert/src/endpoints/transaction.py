from fastapi import APIRouter

router = APIRouter(prefix="/transaction")

@router.post("/create")
def create_transaction():
    pass

@router.post("/send")
def create_transaction():
    pass