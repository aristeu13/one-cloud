from datetime import timedelta, UTC, datetime
from fastapi import HTTPException
from app.application.repository.user_repository import UserRepository
from app.core.settings.setting import Settings


class UserService:
    def __init__(self, repository: UserRepository, settings: Settings):
        self.repository = repository
        self.settings = settings

    def is_within_time_window(self, document):
        now = datetime.now(UTC)
        return (
            document
            and document.get("last_updated")
            and document["last_updated"]
            > (now - timedelta(hours=self.settings.time_window_hour))
        )

    async def update_user(self, user_data: dict):
        await self._update_entity(user_data, role="user", entity="User")

    async def update_admin(self, admin_data: dict):
        await self._update_entity(admin_data, role="admin", entity="Admin")

    async def _update_entity(self, data: dict, role: str, entity: str):
        existing_entity = await self.repository.find_by_email(data["data"]["email"])

        if existing_entity and self.is_within_time_window(existing_entity):
            raise HTTPException(
                status_code=400,
                detail=f"{entity} was updated recently. Please wait before updating again.",
            )

        result = await self.repository.update(data, role=role)
        if not result.matched_count and not result.upserted_id:
            raise HTTPException(
                status_code=500, detail=f"{entity} could not be inserted or updated."
            )

    async def get_user(self):
        return await self._get_entity_by_role("user", "User")

    async def get_admin(self):
        return await self._get_entity_by_role("admin", "Admin")

    async def _get_entity_by_role(self, role: str, entity: str):
        entity_data = await self.repository.find_by_role(role)
        if not entity_data:
            raise HTTPException(status_code=404, detail=f"{entity} not found")
        return entity_data
