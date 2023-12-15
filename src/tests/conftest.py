import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.db.dependancies import get_db
from app.schemas.auth import Token
from app.models.user import User as UserModel

from .session import override_get_db, SessionTest

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


def get_superuser() -> UserModel:
    from app.services.user import UserService
    from app.schemas.user import UserCreate

    from app.utils.service_result import handle_result

    try:
        super_user = handle_result(UserService(SessionTest()).get_user_by_username(username="superuser"))
        return super_user
    except:
        pass

    user = UserCreate(
        username="superuser",
        password="superuser",
        otp_enabled=False,
        is_superuser=True,
        is_active=True,
    )

    super_user = handle_result(UserService(SessionTest()).create_user(obj_in=user))

    return super_user


@pytest.fixture(scope="module")
def superuser_data() -> dict:
    super_user = get_superuser()
    from app.core.auth.jwt import create_access_token

    access_token = create_access_token(user=super_user)

    access_token = access_token.model_dump()

    return {"headers": {"Authorization": f"Bearer {access_token['access_token']}"}, "user": super_user}


