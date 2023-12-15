from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependancies import get_db
from app.utils.service_result import handle_result
from app.core.auth.dependencies import get_current_active_user, get_current_active_superuser

from app.schemas.user import UserCreate, UserUpdate, UserInDB, User as UserSchema
from app.models.user import User as UserModel
from app.services.user import UserService


router = APIRouter()


@router.get("/", response_model=List[UserInDB])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Retrieve users.
    """
    result = UserService(db, current_user).get_users(skip=skip, limit=limit)
    return handle_result(result)


@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Create new user.
    """
    result = UserService(db, current_user).create_user(obj_in=user_in)
    return handle_result(result)


@router.get("/me", response_model=UserSchema)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """
    Get current user.
    """
    print(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific user by id.
    """
    result = UserService(db, current_user).get_user(id=user_id)
    return handle_result(result)


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Update a user.
    """
    result = UserService(db, current_user).update_user(id=user_id, obj_in=user_in)
    return handle_result(result)
