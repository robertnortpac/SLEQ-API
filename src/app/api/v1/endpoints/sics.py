from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.auth.permissions import PermissionChecker
from app.db.dependancies import get_db
from app.utils.service_result import handle_result
from app.models.user import User as UserModel

from app.schemas.sic import SicCreate, SicUpdate, Sic as SicSchema
from app.models.sic import Sic as SicModel
from app.services.sic import SicService

router = APIRouter()

@router.get("/", response_model=List[SicSchema])
def read_sics(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Retrieve sics.
    """
    result = SicService(db, current_user).get_sics(skip=skip, limit=limit)
    return handle_result(result)

@router.post("/", response_model=SicSchema)
def create_sic(
    *,
    db: Session = Depends(get_db),
    sic_in: SicCreate,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Create new sic.
    """
    result = SicService(db, current_user).create_sic(obj_in=sic_in)
    return handle_result(result)

@router.get("/{sic_id}", response_model=SicSchema)
def read_sic_by_id(
    sic_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Get a specific sic by id.
    """
    result = SicService(db, current_user).get_sic(id=sic_id)
    return handle_result(result)

@router.put("/{sic_id}", response_model=SicSchema)
def update_sic(
    *,
    db: Session = Depends(get_db),
    sic_id: str,
    sic_in: SicUpdate,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Update a sic.
    """
    result = SicService(db, current_user).update_sic(id=sic_id, obj_in=sic_in)
    return handle_result(result)

@router.delete("/{sic_id}")
def delete_sic(
    *,
    db: Session = Depends(get_db),
    sic_id: str,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Delete a sic.
    """
    result = SicService(db, current_user).delete_sic(id=sic_id)
    if result:
        return handle_result(result)
    return Response(status_code=204)