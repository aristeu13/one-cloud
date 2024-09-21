import httpx
from fastapi import Depends, HTTPException
from app.core.security.schema import oauth2_scheme
from app.core.settings.setting import Settings, get_settings


class STSService:
    def __init__(self, token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)):
        self.token = token
        self.settings = settings

    async def verify_user_role(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        url = f"{self.settings.external_api}/user"
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token for user role")
            return True

    async def verify_admin_role(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        url = f"{self.settings.external_api}/admin"
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token for admin role")
            return True
