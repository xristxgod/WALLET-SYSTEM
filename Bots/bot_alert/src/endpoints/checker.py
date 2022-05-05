from fastapi import APIRouter

router = APIRouter(prefix="/checker")

@router.post("/bad")
def create_transaction():
    pass

@router.post("/good")
def create_transaction():
    pass