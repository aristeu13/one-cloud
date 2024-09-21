import pytest
import httpx
from unittest.mock import AsyncMock, patch, Mock
from fastapi import HTTPException
from app.application.services.sts_service import STSService
from app.core.settings.setting import Settings


@pytest.mark.asyncio
@patch("app.application.services.sts_service.httpx.AsyncClient")
async def test_verify_user_role_success(mock_async_client_constructor):
    mock_async_client_instance = Mock()

    mock_response = httpx.Response(200)
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)

    mock_async_client_constructor.return_value.__aenter__.return_value = (
        mock_async_client_instance
    )

    mock_settings = Settings(external_api="https://fake.com")
    service = STSService(token="valid_token", settings=mock_settings)

    result = await service.verify_user_role()

    assert result is True

    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/user",
        headers={"Authorization": "Bearer valid_token"},
    )


@pytest.mark.asyncio
@patch("app.application.services.sts_service.httpx.AsyncClient")
async def test_verify_admin_role_success(mock_async_client_constructor):
    mock_async_client_instance = Mock()

    mock_response = httpx.Response(200)
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)

    mock_async_client_constructor.return_value.__aenter__.return_value = (
        mock_async_client_instance
    )

    mock_settings = Settings(external_api="https://fake.com")
    service = STSService(token="valid_token", settings=mock_settings)

    result = await service.verify_admin_role()

    assert result is True

    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/admin",
        headers={"Authorization": "Bearer valid_token"},
    )


@pytest.mark.asyncio
@patch("app.application.services.sts_service.httpx.AsyncClient")
async def test_verify_user_role_invalid_token(mock_async_client_constructor):
    mock_async_client_instance = Mock()

    mock_response = httpx.Response(401)
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)

    mock_async_client_constructor.return_value.__aenter__.return_value = (
        mock_async_client_instance
    )

    mock_settings = Settings(external_api="https://fake.com")
    service = STSService(token="invalid_token", settings=mock_settings)

    with pytest.raises(HTTPException) as exc_info:
        await service.verify_user_role()

    assert exc_info.value.status_code == 401
    assert "Invalid token for user role" in exc_info.value.detail

    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/user",
        headers={"Authorization": "Bearer invalid_token"},
    )


@pytest.mark.asyncio
@patch("app.application.services.sts_service.httpx.AsyncClient")
async def test_verify_admin_role_invalid_token(mock_async_client_constructor):
    mock_async_client_instance = Mock()

    mock_response = httpx.Response(401)
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)

    mock_async_client_constructor.return_value.__aenter__.return_value = (
        mock_async_client_instance
    )

    mock_settings = Settings(external_api="https://fake.com")
    service = STSService(token="invalid_token", settings=mock_settings)

    with pytest.raises(HTTPException) as exc_info:
        await service.verify_admin_role()

    assert exc_info.value.status_code == 401
    assert "Invalid token for admin role" in exc_info.value.detail

    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/admin",
        headers={"Authorization": "Bearer invalid_token"},
    )
