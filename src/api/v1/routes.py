from fastapi import APIRouter

from api.v1.endpoints import companies
from api.v1.endpoints import users
from api.v1.endpoints import rfps
from api.v1.endpoints import roles

router = APIRouter()
router.include_router(companies.router, prefix="/companies", tags=["companies"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(rfps.router, prefix="/rfps", tags=["rfps"])
router.include_router(roles.router, prefix="/roles", tags=["roles"])
