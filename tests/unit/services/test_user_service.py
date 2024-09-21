# tests/unit/test_user_service.py
import pytest
from unittest.mock import AsyncMock
from app.application.services.user_service import UserService
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_update_user_within_time_window():
    mock_repo = AsyncMock()
    mock_settings = AsyncMock()
    mock_settings.time_window_hour = 24

    mock_repo.find_by_email.return_value = {
        "data": {"email": "john@example.com"},
        "last_updated": datetime.now(UTC) - timedelta(hours=1),
    }

    user_service = UserService(repository=mock_repo, settings=mock_settings)

    with pytest.raises(HTTPException) as exc_info:
        await user_service.update_user({"data": {"email": "john@example.com"}})

    assert exc_info.value.status_code == 400
    assert "User was updated recently" in exc_info.value.detail


@pytest.mark.asyncio
async def test_update_user_successful():
    mock_repo = AsyncMock()
    mock_settings = AsyncMock()
    mock_settings.time_window_hour = 24

    mock_repo.find_by_email.return_value = None
    mock_repo.update.return_value = AsyncMock(matched_count=1, upserted_id=None)

    user_service = UserService(repository=mock_repo, settings=mock_settings)

    await user_service.update_user({"data": {"email": "john@example.com"}})

    mock_repo.update.assert_called_once_with(
        {"data": {"email": "john@example.com"}}, role="user"
    )


@pytest.mark.asyncio
async def test_get_user_not_found():
    mock_repo = AsyncMock()
    mock_repo.find_by_role.return_value = None

    user_service = UserService(repository=mock_repo, settings=AsyncMock())

    with pytest.raises(HTTPException) as exc_info:
        await user_service.get_user()

    assert exc_info.value.status_code == 404
    assert "User not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_user_success():
    mock_repo = AsyncMock()
    mock_repo.find_by_role.return_value = {
        "data": {"email": "john@example.com", "name": "John"}
    }

    user_service = UserService(repository=mock_repo, settings=AsyncMock())

    user = await user_service.get_user()

    assert user["data"]["email"] == "john@example.com"
    mock_repo.find_by_role.assert_called_once_with("user")
