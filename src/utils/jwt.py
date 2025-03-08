from datetime import datetime, timezone, timedelta
from typing import List
import uuid
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, security
from src.config import settings
from src.schemas.jwt import JWTTokensResponse, AccessTokenResponse, DecodedToken
class JWTService:


    @staticmethod
    async def create_tokens(user_id: uuid.UUID, scopes: List[str]) -> JWTTokensResponse:
        access_expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_EXPIRE_MINUTES)
        refresh_expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_EXPIRE_DAYS)
        
        base_data = {
            "user_id": str(user_id),
            "scopes": scopes
        }
        
        access_to_encode = base_data.copy()
        access_to_encode.update({
            'exp': access_expire,
            'type': 'access'
        })

        refresh_to_encode = base_data.copy()
        refresh_to_encode.update({
            'exp': refresh_expire,
            'type': 'refresh'
        })
        access_encoded_jwt = jwt.encode(access_to_encode, settings.PRIVATE_KEY, algorithm="RS256")
        refresh_encoded_jwt = jwt.encode(refresh_to_encode, settings.PRIVATE_KEY, algorithm="RS256")

        return JWTTokensResponse(
            access_token=access_encoded_jwt,
            token_type="bearer",
            refresh_token=refresh_encoded_jwt
        )
    @staticmethod
    async def get_current_user(token: str = Depends(security.OAuth2PasswordBearer("/v1/users/login"))):
        try:
            payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=["RS256"])
            if not payload:
                raise HTTPException(status_code=401, detail="User not found")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Could not decode token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return DecodedToken(user_id=payload.get("user_id"), scopes=payload.get("scopes"))
    
    @staticmethod
    async def create_access_token(user_id: uuid.UUID, scopes: List[str]) -> AccessTokenResponse:
        to_encode = {
            "user_id": str(user_id),
            "scopes": scopes
        }
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.PRIVATE_KEY, algorithm="RS256"
        )
        return AccessTokenResponse(
            access_token=encoded_jwt,
            token_type="bearer"
        )
    @staticmethod
    async def decode_refresh_token(token: str):
        try:
            payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=["RS256"])
            
            if payload.get("type")!='refresh':
                raise HTTPException(status_code=401, detail="Invalid token")
            return DecodedToken(user_id=payload.get("user_id"), scopes=payload.get("scopes"))
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Could not decode token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

