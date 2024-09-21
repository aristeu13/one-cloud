from fastapi import APIRouter

from app.application.api.endpoints import user, token, integration, admin

api_router = APIRouter()


api_router.include_router(user.router, tags=["api"])
api_router.include_router(admin.router, tags=["api"])
api_router.include_router(token.router, tags=["auth"])
api_router.include_router(integration.router, tags=["integration"])
