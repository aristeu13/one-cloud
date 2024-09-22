import pytest
import asyncio
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.middleware.auth import check_current_admin, check_current_user
from app.core.middleware.db import get_db
from app.core.settings.client import client


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def override_check_current_admin():
    return True


async def override_check_current_user():
    return True


async def override_get_db():
    db = client["test_db"]
    return db


@pytest_asyncio.fixture(scope="function")
async def client_test():
    app.dependency_overrides[check_current_admin] = override_check_current_admin
    app.dependency_overrides[check_current_user] = override_check_current_user
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    test_db = await override_get_db()

    admin_data = {
        "role": "admin",
        "message": "Hello, admin!",
        "data": {
            "name": "Admin Master",
            "email": "admin@example.com",
            "reports": [
                {"id": 1, "title": "Monthly Sales", "status": "Completed"},
                {"id": 2, "title": "User Activity", "status": "Pending"},
            ],
        },
        "last_updated": None,
    }

    user_data = {
        "role": "user",
        "message": "Hello, user!",
        "data": {
            "name": "John Doe",
            "email": "john@example.com",
            "purchases": [
                {"id": 1, "item": "Laptop", "price": 2500},
                {"id": 2, "item": "Smartphone", "price": 1200},
            ],
        },
        "last_updated": None,
    }

    await test_db["users"].insert_one(admin_data)
    await test_db["users"].insert_one(user_data)

    yield test_db

    await test_db["users"].delete_many({})
