from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from src.models.user import UserModel
from src.schemas.user import CreateUserResponse, CreateUserRequest
from src.api.v1.services.user import UserService
from src.schemas.jwt import JWTTokensResponse, RefreshTokenRequest
from src.utils.jwt import JWTService

router = APIRouter(prefix='/users', tags=['User | v1'])

@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserResponse,
    summary="Register a new user",
    description="Creates a new user account with the provided data."
)
async def sign_up(
    new_user_data: CreateUserRequest,
    service: UserService = Depends(UserService)
):
    return await service.create_user(new_user_data)

@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=JWTTokensResponse,
    summary="Log in a user",
    description="Authenticates a user and returns access and refresh tokens."
)
async def login_user(
    request: Request,
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(UserService)
):
    return await service.login_user(user_data.username, user_data.password, request=request)

@router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    response_model=JWTTokensResponse,
    summary="Refresh user tokens",
    description="Generates new access and refresh tokens using a valid refresh token."
)
async def refresh_tokens(
    request: Request,
    refresh_token: RefreshTokenRequest,
    service: UserService = Depends(UserService)
):
    return await service.refresh_tokens(refresh_token.refresh_token, request=request)

@router.post(
    '/me',
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Returns details of the currently authenticated user."
)
async def me(
    current_user: Annotated[UserModel, Depends(JWTService.get_current_user)]
):
    return current_user

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Log out a user",
    description="Invalidates the user's refresh token to end the session."
)
async def logout(
    request: Request,
    refresh_token: RefreshTokenRequest,
    service: UserService = Depends(UserService)
):
    await service.logout(refresh_token.refresh_token, request=request)