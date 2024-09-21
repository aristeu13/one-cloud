from fastapi import APIRouter
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.application.api.model.user import UserOut
from app.application.repository.user_repository import UserRepository
from app.application.services.user_service import UserService
from app.core.helper.helper import convert_object_id
from app.core.middleware.auth import check_current_user
from app.core.middleware.db import get_db
from app.core.settings.setting import Settings, get_settings

router = APIRouter()


@router.get("/user")
async def get_user(
    _: None = Depends(check_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> UserOut:
    collection = db["users"]

    repository = UserRepository(collection)
    user_admin_service = UserService(repository, settings)

    user_admin = await user_admin_service.get_user()

    return convert_object_id(user_admin)
