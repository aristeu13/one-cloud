import pytest
import pytest_asyncio
from fastapi import HTTPException
from app.main import app
from app.core.middleware.db import get_db
from app.core.middleware.auth import check_current_admin, check_current_user
from app.application.services.external_service import ExternalAPIService
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorDatabase
from conftest import (
    override_get_db,
    override_check_current_admin,
    override_check_current_user,
)


class MockExternalAPIService:
    async def get_user_data(self):
        return {
            "role": "user",
            "message": "Hello, user!",
            "data": {
                "name": "Test User",
                "email": "testuser@example.com",
                "purchases": [
                    {"id": 1, "item": "Book", "price": 10},
                    {"id": 2, "item": "Pen", "price": 2},
                ],
            },
            "last_updated": None,
        }

    async def get_admin_data(self):
        return {
            "role": "admin",
            "message": "Hello, admin!",
            "data": {
                "name": "Test Admin",
                "email": "testadmin@example.com",
                "reports": [
                    {"id": 1, "title": "Weekly Report", "status": "Completed"},
                    {"id": 2, "title": "Daily Report", "status": "Pending"},
                ],
            },
            "last_updated": None,
        }


class MockExternalAPIServiceError:
    async def get_user_data(self):
        raise HTTPException(status_code=500, detail="External API error")

    async def get_admin_data(self):
        raise HTTPException(status_code=500, detail="External API error")


def get_mock_external_api_service():
    return MockExternalAPIService()


def get_mock_external_api_service_error():
    return MockExternalAPIServiceError()


@pytest_asyncio.fixture(scope="function")
async def client_integration_test():
    app.dependency_overrides[ExternalAPIService] = get_mock_external_api_service
    app.dependency_overrides[check_current_admin] = override_check_current_admin
    app.dependency_overrides[check_current_user] = override_check_current_user
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def setup_integration_database():
    test_db = await override_get_db()
    await test_db["users"].delete_many({})
    yield test_db
    await test_db["users"].delete_many({})


@pytest.mark.asyncio
async def test_integration_user(client_integration_test, setup_integration_database):
    response = await client_integration_test.post("/integration/user")
    assert response.status_code == 204
    db = await override_get_db()
    user = await db["users"].find_one({"data.email": "testuser@example.com"})
    assert user is not None
    assert user["data"]["name"] == "Test User"
    assert user["role"] == "user"
    assert user["message"] == "Hello, user!"


@pytest.mark.asyncio
async def test_integration_admin(client_integration_test, setup_integration_database):
    response = await client_integration_test.post("/integration/admin")
    assert response.status_code == 204
    db = await override_get_db()
    admin = await db["users"].find_one({"data.email": "testadmin@example.com"})
    assert admin is not None
    assert admin["data"]["name"] == "Test Admin"
    assert admin["role"] == "admin"
    assert admin["message"] == "Hello, admin!"


@pytest.mark.asyncio
async def test_integration_user_api_error(client_integration_test):
    app.dependency_overrides[ExternalAPIService] = get_mock_external_api_service_error
    response = await client_integration_test.post("/integration/user")
    assert response.status_code == 500
    assert response.json()["detail"] == "External API error"


@pytest.mark.asyncio
async def test_integration_admin_api_error(client_integration_test):
    app.dependency_overrides[ExternalAPIService] = get_mock_external_api_service_error
    response = await client_integration_test.post("/integration/admin")
    assert response.status_code == 500
    assert response.json()["detail"] == "External API error"
