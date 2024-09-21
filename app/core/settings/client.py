import motor.motor_asyncio

from app.core.settings.setting import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
