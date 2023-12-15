from fastapi.testclient import TestClient

from app.models.user import User as UserModel
from app.schemas.user import UserCreate


def test_create_user(test_app: TestClient, superuser_data):
    user = UserCreate(
        username="testuser",
        password="testpassword",
        otp_enabled=False,
        is_superuser=False,
        is_active=True,
    )
    response = test_app.post(
        "/api/v1/users/", json=user.model_dump(), headers=superuser_data["headers"]
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_create_user_existing_username(test_app: TestClient, superuser_data):
    user = UserCreate(
        username="testuser",
        password="testpassword",
        otp_enabled=False,
        is_superuser=False,
        is_active=True,
    )
    response = test_app.post(
        "/api/v1/users/", json=user.model_dump(), headers=superuser_data["headers"]
    )
    assert response.status_code == 409
    assert response.json()["app_exception"] == "UserAlreadyExists"


def test_list_users(test_app: TestClient, superuser_data):
    response = test_app.get("/api/v1/users/", headers=superuser_data["headers"])
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["username"] == "superuser"


def test_get_user(test_app: TestClient, superuser_data):
    response = test_app.get(f"/api/v1/users/{superuser_data['user'].id}", headers=superuser_data["headers"])
    assert response.status_code == 200
    assert response.json()["username"] == "superuser"
