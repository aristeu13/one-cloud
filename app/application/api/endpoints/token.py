from fastapi import APIRouter
from fastapi.params import Depends

from app.application.api.model.token import TokenOut
from app.core.middleware.auth import get_token

router = APIRouter()


@router.post("/token")
def create_token(token: dict = Depends(get_token)):
    return TokenOut(**token)
