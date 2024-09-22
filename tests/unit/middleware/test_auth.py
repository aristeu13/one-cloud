import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.core.middleware.auth import get_token, check_current_user, check_current_admin
from app.core.settings.setting import get_settings
from app.application.services.sts_service import STSService
from fastapi.security import OAuth2PasswordRequestForm
from httpx import Response, RequestError, HTTPStatusError


@pytest_asyncio.fixture
async def mock_settings():
    class MockSettings:
        external_api = "http://testapi.com"

    return MockSettings()


@pytest.mark.asyncio
async def test_get_token_success(mock_settings):
    form_data = OAuth2PasswordRequestForm(
        username="testuser",
        password="testpass",
        scope="",
        client_id=None,
        client_secret=None,
    )

    async def mock_post(*args, **kwargs):
        return Response(
            status_code=200, json={"access_token": "testtoken", "token_type": "bearer"}
        )

    with patch("httpx.AsyncClient.post", new=mock_post):
        token = await get_token(form_data=form_data, settings=mock_settings)
        assert token == {"access_token": "testtoken", "token_type": "bearer"}


@pytest.mark.asyncio
async def test_get_token_failure(mock_settings):
    form_data = OAuth2PasswordRequestForm(
        username="testuser",
        password="wrongpass",
        scope="",
        client_id=None,
        client_secret=None,
    )

    async def mock_post(*args, **kwargs):
        return Response(status_code=401)

    with patch("httpx.AsyncClient.post", new=mock_post):
        with pytest.raises(HTTPException) as exc_info:
            await get_token(form_data=form_data, settings=mock_settings)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Failed to retrieve token"


@pytest.mark.asyncio
async def test_get_token_request_error(mock_settings):
    form_data = OAuth2PasswordRequestForm(
        username="testuser",
        password="testpass",
        scope="",
        client_id=None,
        client_secret=None,
    )

    async def mock_post(*args, **kwargs):
        raise RequestError("Request failed")

    with patch("httpx.AsyncClient.post", new=mock_post):
        with pytest.raises(HTTPException) as exc_info:
            await get_token(form_data=form_data, settings=mock_settings)
        assert exc_info.value.status_code == 503
        assert exc_info.value.detail == "External authentication service is unavailable"


@pytest.mark.asyncio
async def test_get_token_http_status_error(mock_settings):
    form_data = OAuth2PasswordRequestForm(
        username="testuser",
        password="testpass",
        scope="",
        client_id=None,
        client_secret=None,
    )

    async def mock_post(*args, **kwargs):
        response = Response(status_code=500)
        raise HTTPStatusError("Server error", request=None, response=response)

    with patch("httpx.AsyncClient.post", new=mock_post):
        with pytest.raises(HTTPException) as exc_info:
            await get_token(form_data=form_data, settings=mock_settings)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Unexpected error from external service"


@pytest.mark.asyncio
async def test_check_current_user_success():
    mock_sts = AsyncMock()
    mock_sts.verify_user_role = AsyncMock()
    await check_current_user(sts=mock_sts)
    mock_sts.verify_user_role.assert_awaited_once()


@pytest.mark.asyncio
async def test_check_current_user_failure():
    mock_sts = AsyncMock()
    mock_sts.verify_user_role = AsyncMock(
        side_effect=HTTPException(status_code=403, detail="Forbidden")
    )
    with pytest.raises(HTTPException) as exc_info:
        await check_current_user(sts=mock_sts)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Forbidden"
    mock_sts.verify_user_role.assert_awaited_once()


@pytest.mark.asyncio
async def test_check_current_admin_success():
    mock_sts = AsyncMock()
    mock_sts.verify_admin_role = AsyncMock()
    await check_current_admin(sts=mock_sts)
    mock_sts.verify_admin_role.assert_awaited_once()


@pytest.mark.asyncio
async def test_check_current_admin_failure():
    mock_sts = AsyncMock()
    mock_sts.verify_admin_role = AsyncMock(
        side_effect=HTTPException(status_code=403, detail="Forbidden")
    )
    with pytest.raises(HTTPException) as exc_info:
        await check_current_admin(sts=mock_sts)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Forbidden"
    mock_sts.verify_admin_role.assert_awaited_once()
