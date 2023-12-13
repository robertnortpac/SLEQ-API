from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from db.dependancies import get_db
from core.auth.dependencies import get_current_active_user, get_current_active_superuser


from schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyInDB,
    Company as CompanySchema,
)
from schemas.user import User as UserSchema
from models.user import User as UserModel
from services.company import CompanyService

from utils.service_result import handle_result

router = APIRouter()


@router.get("/", response_model=List[CompanySchema])
def read_companies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Retrieve companies.
    """
    result = CompanyService(db, current_user).get_companies(skip=skip, limit=limit)
    return handle_result(result)


@router.post("/", response_model=CompanySchema)
def create_company(
    *,
    db: Session = Depends(get_db),
    company_in: CompanyCreate,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Create new company.
    """
    result = CompanyService(db, current_user).create_company(obj_in=company_in)
    return handle_result(result)


@router.get("/{company_id}", response_model=CompanySchema)
def read_company_by_id(
    company_id: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific company by id.
    """
    result = CompanyService(db, current_user).get_company(id=company_id)
    return handle_result(result)


@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    *,
    db: Session = Depends(get_db),
    company_id: str,
    company_in: CompanyUpdate,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Update a company.
    """
    result = CompanyService(db, current_user).update_company(
        id=company_id, obj_in=company_in
    )
    return handle_result(result)


@router.delete(
    "/{company_id}", responses={204: {
        "description": "Company deleted"
    }}, status_code=HTTP_204_NO_CONTENT
)
def delete_company(
    *,
    db: Session = Depends(get_db),
    company_id: str,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    """
    Delete a company.
    """
    result = CompanyService(db, current_user).delete_company(id=company_id)
    if result:
        return handle_result(result)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/{company_id}/users", response_model=List[UserSchema])
def read_company_users(
    company_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific company by id.
    """
    result = CompanyService(db, current_user).get_company_users(
        id=company_id, skip=skip, limit=limit
    )
    return handle_result(result)
