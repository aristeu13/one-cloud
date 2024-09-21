import pytest
import httpx
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch, Mock
from app.application.services.external_service import ExternalAPIService
from app.core.settings.setting import Settings


@pytest.mark.asyncio
@patch("app.application.services.external_service.httpx.AsyncClient")
async def test_get_user_data_success(mock_async_client_constructor):
    mock_async_client_instance = Mock()
    
    mock_response = httpx.Response(200, json={"name": "John Doe", "email": "john@example.com"})
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)
    
    mock_async_client_constructor.return_value.__aenter__.return_value = mock_async_client_instance

    mock_settings = Settings(external_api="https://fake.com")
    service = ExternalAPIService(token="fake_token", settings=mock_settings)
    
    user_data = await service.get_user_data()
    
    assert user_data["email"] == "john@example.com"
    
    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/user",
        headers={"Authorization": "Bearer fake_token"},
    )


@pytest.mark.asyncio
@patch("app.application.services.external_service.httpx.AsyncClient")
async def test_get_admin_data_success(mock_async_client_constructor):
    
    mock_async_client_instance = Mock()
    
    mock_response = httpx.Response(200, json={"name": "Admin Master", "email": "admin@example.com"})
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)
    
    mock_async_client_constructor.return_value.__aenter__.return_value = mock_async_client_instance

    mock_settings = Settings(external_api="https://fake.com")
    service = ExternalAPIService(token="fake_token", settings=mock_settings)
    
    admin_data = await service.get_admin_data()
    assert admin_data["email"] == "admin@example.com"
    
    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/admin",
        headers={"Authorization": "Bearer fake_token"},
    )


@pytest.mark.asyncio
@patch("app.application.services.external_service.httpx.AsyncClient")
async def test_get_user_data_failure(mock_async_client_constructor):
    mock_async_client_instance = Mock()
    
    mock_response = httpx.Response(500)
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)
    
    mock_async_client_constructor.return_value.__aenter__.return_value = mock_async_client_instance

    mock_settings = Settings(external_api="https://fake.com")
    service = ExternalAPIService(token="fake_token", settings=mock_settings)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_data()
    
    assert exc_info.value.status_code == 500
    assert "Failed to fetch data from user" in exc_info.value.detail
    
    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/user",
        headers={"Authorization": "Bearer fake_token"},
    )


@pytest.mark.asyncio
@patch("app.application.services.external_service.httpx.AsyncClient")
async def test_get_admin_data_failure(mock_async_client_constructor):
    mock_async_client_instance = Mock()
    
    mock_response = httpx.Response(404)
    mock_async_client_instance.get = AsyncMock(return_value=mock_response)
    
    mock_async_client_constructor.return_value.__aenter__.return_value = mock_async_client_instance

    mock_settings = Settings(external_api="https://fake.com")
    service = ExternalAPIService(token="fake_token", settings=mock_settings)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_admin_data()
    
    assert exc_info.value.status_code == 404
    assert "Failed to fetch data from admin" in exc_info.value.detail
    
    mock_async_client_instance.get.assert_called_once_with(
        "https://fake.com/admin",
        headers={"Authorization": "Bearer fake_token"},
    )
