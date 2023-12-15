from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.auth.permissions import PermissionChecker
from app.db.dependancies import get_db
from app.utils.service_result import handle_result
from app.models.user import User as UserModel

from app.schemas.tpa import TpaCreate, TpaUpdate, Tpa as TpaSchema
from app.models.tpa import Tpa as TpaModel
from app.services.tpa import TpaSevice

router = APIRouter()

@router.get("/", response_model=List[TpaSchema])
def read_tpas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Retrieve tpas.
    """
    result = TpaSevice(db, current_user).get_tpas(skip=skip, limit=limit)
    return handle_result(result)

@router.post("/", response_model=TpaSchema)
def create_tpa(
    *,
    db: Session = Depends(get_db),
    tpa_in: TpaCreate,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Create new tpa.
    """
    result = TpaSevice(db, current_user).create_tpa(obj_in=tpa_in)
    return handle_result(result)

@router.get("/{tpa_id}", response_model=TpaSchema)
def read_tpa_by_id(
    tpa_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Get a specific tpa by id.
    """
    result = TpaSevice(db, current_user).get_tpa(id=tpa_id)
    return handle_result(result)

@router.put("/{tpa_id}", response_model=TpaSchema)
def update_tpa(
    *,
    db: Session = Depends(get_db),
    tpa_id: str,
    tpa_in: TpaUpdate,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Update a tpa.
    """
    result = TpaSevice(db, current_user).update_tpa(id=tpa_id, obj_in=tpa_in)
    return handle_result(result)

@router.delete("/{tpa_id}")
def delete_tpa(
    *,
    db: Session = Depends(get_db),
    tpa_id: str,
    current_user: UserModel = Depends(PermissionChecker([])),
):
    """
    Delete a tpa.
    """
    result = TpaSevice(db, current_user).delete_tpa(id=tpa_id)
    if result:
        return handle_result(result)
    return Response(status_code=204)
