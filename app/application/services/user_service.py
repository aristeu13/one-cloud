from datetime import timedelta, UTC, datetime
from fastapi import HTTPException

from app.application.repository.user_repository import UserRepository
from app.core.settings.setting import Settings

class   UserService:
    def __init__(self, repository: UserRepository, settings: Settings):
        self.repository = repository
        self.settings = settings

    def is_within_time_window(self, document):
        now = datetime.now(UTC)
        return document and document.get("last_updated") and \
               document["last_updated"] > (now - timedelta(hours=self.settings.time_window_hour))

    async def update_user(self, user_data: dict):
        existing_user = await self.repository.find_by_email(user_data["data"]["email"])

        if existing_user and self.is_within_time_window(existing_user):
            raise HTTPException(status_code=400, detail="User was updated recently. Please wait before updating again.")

        result = await self.repository.update(user_data, role="user")
        if not result.matched_count and not result.upserted_id:
            raise HTTPException(status_code=500, detail="User could not be inserted or updated.")

    async def update_admin(self, admin_data: dict):
        existing_admin = await self.repository.find_by_email(admin_data["data"]["email"])

        if existing_admin and self.is_within_time_window(existing_admin):
            raise HTTPException(status_code=400, detail="Admin was updated recently. Please wait before updating again.")

        result = await self.repository.update(admin_data, role="admin")
        if not result.matched_count and not result.upserted_id:
            raise HTTPException(status_code=500, detail="Admin could not be inserted or updated.")

    async def get_user(self):
        user = await self.repository.find_by_role("user")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_admin(self):
        user = await self.repository.find_by_role("admin")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
