import httpx
from fastapi import Depends, HTTPException
from app.core.security.schema import oauth2_scheme
from app.core.settings.setting import Settings, get_settings


class ExternalAPIService:
    def __init__(
        self,
        token: str = Depends(oauth2_scheme),
        settings: Settings = Depends(get_settings),
    ):
        self.token = token
        self.settings = settings

    async def _fetch_data(self, endpoint: str):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        url = f"{self.settings.external_api}/{endpoint}"
        
        async with httpx.AsyncClient(verify=False, timeout=10) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch data from {endpoint}.",
                )
            return response.json()

    async def get_user_data(self):
        return await self._fetch_data("user")

    async def get_admin_data(self):
        return await self._fetch_data("admin")
