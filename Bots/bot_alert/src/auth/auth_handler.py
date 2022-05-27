from typing import Dict

import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import Config, logger

class AutoHandler:
    @staticmethod
    def sign_jwt_token() -> Dict[str, str]:
        return jwt.encode(
            {"token": Config.BOT_ALERT_JWT_NAME}, Config.BOT_ALERT_JWT_SECRET, algorithm=Config.BOT_ALERT_JWT_ALGORITHM
        )

    @staticmethod
    def decode_jwt_token(token: str) -> Dict:
        try:
            return jwt.decode(token, Config.BOT_ALERT_JWT_SECRET, algorithm=Config.BOT_ALERT_JWT_ALGORITHM)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return {}

    @staticmethod
    def is_valid(token: str) -> bool:
        payload = AutoHandler.decode_jwt_token(token)
        if payload:
            return True

class JWTBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid token!")
            if not AutoHandler.is_valid(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid token!")