from fastapi import HTTPException, Depends
import httpx
from fastapi.security import OAuth2PasswordRequestForm

from app.application.services.sts_service import STSService
from app.core.security.schema import oauth2_scheme
from app.core.settings.setting import get_settings, Settings


async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings),
) -> dict:
    params = {"username": form_data.username, "password": form_data.password}
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                f"{settings.external_api}/token", params=params
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail="Failed to retrieve token"
                )

            return response.json()

    except httpx.RequestError:
        raise HTTPException(
            status_code=503, detail="External authentication service is unavailable"
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail="Unexpected error from external service",
        )


async def check_current_user(sts: STSService = Depends(STSService)):
    await sts.verify_user_role()


async def check_current_admin(sts: STSService = Depends(STSService)):
    await sts.verify_admin_role()
