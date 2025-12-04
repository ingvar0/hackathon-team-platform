from fastapi import Cookie, Depends, HTTPException
from backend.admin.models import Admin
from backend.config import settings
from backend.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import jwt


def get_current_telegram_id(
    access_token: str | None = Cookie(default=None)
) -> str:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    telegram_id = payload.get("telegram_id")
    if telegram_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return str(telegram_id)



async def get_current_admin(
    admin_access_token: str = Cookie(None),
    session: AsyncSession = Depends(get_db),
):
    if not admin_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            admin_access_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        admin_id = payload.get("sub")
        if admin_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    admin = await session.get(Admin, int(admin_id))
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")

    return admin

