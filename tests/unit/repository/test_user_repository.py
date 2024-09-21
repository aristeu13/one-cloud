import pytest
from unittest.mock import AsyncMock, ANY
from app.application.repository.user_repository import UserRepository


@pytest.mark.asyncio
async def test_find_by_email():
    mock_collection = AsyncMock()

    repository = UserRepository(mock_collection)

    mock_collection.find_one.return_value = {
        "data": {"email": "john@example.com"},
        "role": "user",
    }

    result = await repository.find_by_email("john@example.com")

    assert result["data"]["email"] == "john@example.com"

    mock_collection.find_one.assert_called_once_with({"data.email": "john@example.com"})


@pytest.mark.asyncio
async def test_find_by_role():
    mock_collection = AsyncMock()

    repository = UserRepository(mock_collection)

    mock_collection.find_one.return_value = {
        "data": {"email": "admin@example.com"},
        "role": "admin",
    }

    result = await repository.find_by_role("admin")

    assert result["role"] == "admin"

    mock_collection.find_one.assert_called_once_with({"role": "admin"})


@pytest.mark.asyncio
async def test_update():
    mock_collection = AsyncMock()

    repository = UserRepository(mock_collection)

    mock_collection.update_one.return_value = AsyncMock(
        matched_count=1, upserted_id=None
    )

    user_data = {"data": {"email": "john@example.com", "name": "John Doe"}}

    result = await repository.update(user_data, role="user")

    mock_collection.update_one.assert_called_once_with(
        {"data.email": "john@example.com"},
        {"$set": {**user_data, "role": "user", "last_updated": ANY}},
        upsert=True,
    )

    assert result.matched_count == 1
