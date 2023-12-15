from fastapi import Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.core.auth.dependencies import get_current_user
from app.models.user import User

class PermissionChecker:
    """
    Permission checker class.
    """

    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.is_superuser:
            return user
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions to perform this action.",
        )
        for permission in self.required_permissions:
            if permission not in user.permissions:
                return False