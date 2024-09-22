import pytest
import pytest_asyncio
from app.main import app
from app.core.middleware.auth import get_token
from httpx import AsyncClient, ASGITransport


def override_get_token():
    return {"access_token": "test_access_token", "token_type": "bearer"}


@pytest_asyncio.fixture(scope="function")
async def client_token_test():
    app.dependency_overrides[get_token] = override_get_token
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_token(client_token_test):
    response = await client_token_test.post("/token")
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test_access_token",
        "token_type": "bearer",
    }
