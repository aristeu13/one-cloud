from datetime import datetime, UTC
from motor.motor_asyncio import AsyncIOMotorCollection


class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def find_by_email(self, email: str):
        return await self.collection.find_one({"data.email": email})

    async def find_by_role(self, role: str):
        return await self.collection.find_one({"role": role})

    async def update(self, data: dict, role: str):
        now = datetime.now(UTC)
        data["role"] = role
        result = await self.collection.update_one(
            {"data.email": data["data"]["email"]},
            {"$set": {**data, "last_updated": now}},
            upsert=True,
        )
        return result
