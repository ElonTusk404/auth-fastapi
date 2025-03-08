from typing import List
from pydantic import BaseModel

class JWTTokensResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    
    class Config:
        arbitrary_types_allowed = True


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        arbitrary_types_allowed = True


class DecodedToken(BaseModel):
    user_id: str
    scopes: List[str]
    
    class Config:
        arbitrary_types_allowed = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str
