from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel
from core.configs import settings
from core.security import verify_password

from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1}/users/login"
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


def _create_token(token_type: str, ttl: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3

    payload = {}

    tz_sp = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=tz_sp) + ttl

    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.now(tz_sp)
    payload["sub"] = sub

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    """
    https://jwt.io
    """

    return _create_token(
        token_type='access_token',
        ttl=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )