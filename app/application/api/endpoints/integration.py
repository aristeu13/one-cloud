from fastapi import HTTPException, APIRouter, Depends

from app.application.repository.user_repository import UserRepository
from app.application.services.external_service import ExternalAPIService
from app.application.services.user_service import UserService
from app.core.middleware.db import get_db
from app.core.settings.setting import Settings, get_settings
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.post("/integration/user", status_code=204)
async def get_data_from_integration_and_create(
        db: AsyncIOMotorDatabase = Depends(get_db),
        api_service: ExternalAPIService = Depends(),
        settings: Settings = Depends(get_settings),
):
    collection = db["users"]

    repository = UserRepository(collection)
    user_admin_service = UserService(repository, settings)

    try:
        user_data = await api_service.get_user_data()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    await user_admin_service.update_user(user_data)

    return None


@router.post("/integration/admin", status_code=204)
async def get_data_from_integration_and_create(
        db: AsyncIOMotorDatabase = Depends(get_db),
        api_service: ExternalAPIService = Depends(),
        settings: Settings = Depends(get_settings),
):
    collection = db["users"]

    repository = UserRepository(collection)
    user_admin_service = UserService(repository, settings)

    try:
        admin_data = await api_service.get_admin_data()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    await user_admin_service.update_admin(admin_data)

    return None
