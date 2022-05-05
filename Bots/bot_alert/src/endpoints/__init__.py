from fastapi import APIRouter

from src.endpoints import transaction, user, checker

router = APIRouter(prefix="/api")

# Include router Transaction
router.include_router(transaction.router)
# Include router User
router.include_router(user.router)
# Include router Checker
router.include_router(checker.router)
