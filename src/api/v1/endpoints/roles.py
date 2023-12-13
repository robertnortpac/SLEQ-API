from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud.role as crud
from schemas.role import RoleCreate, Role as RoleSchema
from models.role import Role
from schemas.user import User

from db.dependancies import get_db
from core.auth.dependencies import get_current_active_user, get_current_active_superuser

router = APIRouter()

@router.get("/", response_model=List[RoleSchema])
def read_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Retrieve roles.
    """
    roles = crud.role.get_multi(db, skip=skip, limit=limit)
    return roles

@router.post("/", response_model=RoleSchema)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Create new role.
    """
    role = crud.role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system.",
        )
    role = crud.role.create(db, obj_in=role_in)
    return role

@router.get("/{role_id}", response_model=RoleSchema)
def read_role_by_id(
    role_id: str,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
):
    """
    Get a specific role by id.
    """
    role = crud.role.get(db, id=role_id)
    return role