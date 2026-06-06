import time
from typing import Annotated
from uuid import uuid4

from jose import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.config import settings


class TokenPayload(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


def sign_jwt(user_id: int) -> dict:
    now = time.time()
    payload = {
        "iss": "desafio-bank.com.br",
        "sub": user_id,
        "aud": "desafio-bank",
        "exp": now + (60 * 30),  # 30 minutes
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return {"access_token": token, "token_type": "Bearer"}


async def decode_jwt(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.secret_key, audience="desafio-bank", algorithms=[settings.algorithm])
        return TokenPayload.model_validate(payload)
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenPayload:
        auth_credentials = await super().__call__(request)
        if not auth_credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )

        payload = await decode_jwt(auth_credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )
        return payload


async def get_current_user(
    token: Annotated[TokenPayload, Depends(JWTBearer())],
) -> dict[str, int]:
    return {"user_id": token.sub}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user