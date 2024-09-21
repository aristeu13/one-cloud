from fastapi.params import Depends

from app.core.security.schema import oauth2_scheme


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"role": "user"}
