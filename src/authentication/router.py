from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.app.database.database import get_repository
from src.app.core.config import get_app_settings
from src.app.core.settings.app import AppSettings
from src.app.exceptions import EntityDoesNotExist
from src.authentication.repository import UsersRepository
from src.authentication.schema import (
    UserInCreate,
    UserInLogin,
    UserInResponse,
    UserWithToken,
)
from src.authentication import service
from src.authentication.service import (
    check_email_is_taken,
    check_username_is_taken,
)
from src.utils.responses.http_success import response_success
from src.utils.responses.schema import ResponseModel

router = APIRouter()

@router.post(
        "/login", 
        name="auth:login",
        response_model=ResponseModel[UserInResponse],
        )
async def login(
    user_login: UserInLogin = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
):
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="Incorrect email or password",
    )

    try:
        user = await users_repo.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = service.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )

    user_with_token = UserWithToken(
        username=user.username,
        email=user.email,
        bio=user.bio,
        image=user.image,
        token=token,
    )

    return response_success(
        status_code=HTTP_200_OK,
        message="Login Success",
        data=UserInResponse(user=user_with_token).dict(),
    )

@router.post(
        "/register", 
        status_code=HTTP_201_CREATED, 
        name="auth:register",        
        response_model=ResponseModel[UserInResponse],
        )
async def register(
    user_create: UserInCreate = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
):
    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = await users_repo.create_user(**user_create.dict())

    token = service.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )

    user_with_token = UserWithToken(
        username=user.username,
        email=user.email,
        bio=user.bio,
        image=user.image,
        token=token,
    )

    return response_success(
        status_code=HTTP_201_CREATED,
        message="Register Success",
        data=UserInResponse(user=user_with_token).dict(),
    )
