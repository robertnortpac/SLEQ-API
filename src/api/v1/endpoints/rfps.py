from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models.user import User

import crud.rfp as crud
from models.rfp import Rfp
import schemas.rfp as schemas
from db.dependancies import get_db
from core.auth.dependencies import get_current_active_user, get_current_active_superuser

router = APIRouter()

@router.post("/", response_model=schemas.Rfp)
def create_rfp(
    *,
    db: Session = Depends(get_db),
    rfp_in: schemas.RfpCreate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create new rfp.
    """
    rfp = crud.rfp.is_unique(db, obj_in=rfp_in)
    if not rfp:
        raise HTTPException(
            status_code=400,
            detail="The rfp with this information already exists in the system.",
        )
    rfp = crud.rfp.create(db, obj_in=rfp_in, current_user=current_user)
    return rfp

@router.get("/", response_model=List[schemas.Rfp])
def read_rfps(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Retrieve rfps.
    """
    rfps = crud.rfp.get_multi(db, skip=skip, limit=limit)
    return rfps

@router.get("/mine", response_model=List[schemas.Rfp])
def read_my_rfps(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve my rfps.
    """
    rfps = crud.rfp.get_by_user(db, user_id=current_user.id)
    return rfps