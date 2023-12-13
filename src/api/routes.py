from fastapi import APIRouter

router = APIRouter()

from api.endpoints import auth
router.include_router(auth.router, prefix="/auth", tags=["auth"])