from fastapi import APIRouter

from app.api.v1.endpoints import companies
from app.api.v1.endpoints import users
from app.api.v1.endpoints import roles
from app.api.v1.endpoints import tpas
from app.api.v1.endpoints import sics
from app.api.v1.endpoints import rfps



router = APIRouter()
router.include_router(companies.router, prefix="/companies", tags=["companies"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(roles.router, prefix="/roles", tags=["roles"])
router.include_router(tpas.router, prefix="/tpas", tags=["tpas"])
router.include_router(sics.router, prefix="/sics", tags=["sics"])
router.include_router(rfps.router, prefix="/rfps", tags=["rfps"])

