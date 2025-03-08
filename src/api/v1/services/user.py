
from fastapi import HTTPException, status, Request

from src.models import UserModel
from src.utils.hash import get_password_hash, verify_password
from src.schemas.user import CreateUserRequest, CreateUserResponse
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.schemas.jwt import JWTTokensResponse
from src.utils.jwt import JWTService


class UserService(BaseService):
    base_repository: str = 'user'

    @transaction_mode
    async def create_user(self, user: CreateUserRequest) -> CreateUserResponse:
        """Create user."""
        exists_user = await self.uow.user.get_by_query_one_or_none(username=user.username)
        if exists_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
        user.password = get_password_hash(user.password)
        return await self.uow.user.add_one_and_get_obj(**user.model_dump())
    
    @transaction_mode
    async def login_user(self, username: str, password: str, request: Request):
        user: UserModel = await self.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        tokens : JWTTokensResponse = await JWTService.create_tokens(user_id=user.id, scopes=user.scopes)
        await self.uow.token.add_one(user_id=user.id, token = tokens.refresh_token, ip_address=request.client.host, user_agent=request.headers.get('user-agent'))
        return tokens


    @transaction_mode
    async def authenticate_user(self, username: str, password: str):
        user: UserModel = await self.uow.user.get_by_query_one_or_none(username = username)
        
        if not (user and verify_password(plain_password=password, hashed_password=user.password)):
            return None
        return user
    
    @transaction_mode
    async def refresh_tokens(self, refresh_token: str, request: Request):
        token = await self.uow.token.get_by_query_one_or_none(token=refresh_token, is_revoked=False, ip_address=request.client.host, user_agent=request.headers.get('user-agent'))
        if not token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user: UserModel = await self.uow.user.get_by_query_one_or_none(id=token.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await self.uow.token.delete_by_query(token=refresh_token)
        tokens: JWTTokensResponse = await JWTService.create_tokens(user_id=user.id, scopes=user.scopes)
        await self.uow.token.add_one(user_id=user.id, token=tokens.refresh_token, ip_address=request.client.host, user_agent=request.headers.get('user-agent'))
        return tokens
    
    @transaction_mode
    async def logout(self, refresh_token: str, request: Request):
        exists_token = await self.uow.token.get_by_query_one_or_none(token=refresh_token, is_revoked=False, ip_address=request.client.host, user_agent=request.headers.get('user-agent'))
        if not exists_token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await self.uow.token.delete_by_query(token=refresh_token)
        return None
    