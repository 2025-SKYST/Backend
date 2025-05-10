from fastapi import APIRouter, Depends, Response, Request, HTTPException
from typing import Annotated, Optional
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mysol.app.user.dto.requests import UserSignupRequest, UserSigninRequest, TokenRefreshRequest, UserUpdateRequest
from mysol.app.user.dto.reponses import UserSignupResponse, UserSigninResponse, MyProfileResponse, RefreshResponse
from mysol.app.user.service import UserService
from mysol.app.user.models import User
from mysol.app.user.errors import InvalidTokenError, MissingAccessTokenError
from datetime import datetime, timezone

user_router = APIRouter()
security = HTTPBearer(auto_error=False)  # 🔹 헤더에서 Bearer 토큰을 읽기 위한 FastAPI 보안 모듈

async def get_current_user_from_header(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: Annotated[UserService, Depends()]
) -> User:
    """
    `Authorization: Bearer <access_token>` 헤더에서 JWT를 추출하여 사용자 인증.
    """
    if not credentials:
        raise MissingAccessTokenError()

    access_token = credentials.credentials  # Bearer 토큰 추출
    email = user_service.validate_access_token(access_token)  # 토큰 검증 및 사용자 이메일 확인
    user = await user_service.get_user_by_email(email)

    if not user:
        raise InvalidTokenError()
    
    return user

async def get_current_user_from_header_optional(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
    user_service: Annotated[UserService, Depends()]
) -> Optional[User]:
    """
    Authorization 헤더에 Bearer 토큰이 있다면 해당 토큰을 검증하여 User를 반환하고,
    없거나 검증 실패 시 None을 반환합니다.
    """
    if not credentials:
        return None

    access_token = credentials.credentials  # Bearer 토큰 추출
    try:
        email = user_service.validate_access_token(access_token)  # 토큰 검증 및 이메일 확인
        user = await user_service.get_user_by_email(email)
        if not user:
            return None
        return user
    except Exception:
        # 토큰 검증 실패 시 None 반환 (추후 로깅 등 추가 가능)
        return None

@user_router.post("/signup", response_model=UserSignupResponse, status_code=HTTP_201_CREATED)
async def signup(
    signup_request: UserSignupRequest,
    user_service: Annotated[UserService, Depends()]
) -> UserSignupResponse:
    """
    새로운 사용자를 등록하는 API.
    """
    birth = signup_request.to_birth_datetime()

    user = await user_service.add_user(
        username=signup_request.username,
        login_id=signup_request.login_id,
        password=signup_request.password,
        birth=birth,
    )

    return UserSignupResponse(
        username=user.username,
        email=user.email
    )


@user_router.post("/signin", status_code=HTTP_200_OK)
async def signin(
    user_service: Annotated[UserService, Depends()],
    signin_request: UserSigninRequest,
):
    """
    로그인 API: access_token 및 refresh_token 발급.
    JWT는 Authorization 헤더를 통해 전달.
    """
    access_token, refresh_token = await user_service.signin(
        signin_request.email, signin_request.password
    )

    user= await user_service.get_user_by_email(signin_request.email)

    return UserSigninResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@user_router.post("/refresh", status_code=HTTP_200_OK)
async def refresh(
    refresh_request: TokenRefreshRequest,
    user_service: Annotated[UserService, Depends()],
) -> RefreshResponse:
    """
    `refresh_token`을 이용해 `access_token`을 재발급하는 API.
    기존 `refresh_token`을 블랙리스트에 추가하여 재사용 방지.
    """
    refresh_token = refresh_request.refresh_token

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    
    access_token, new_refresh_token = await user_service.reissue_tokens(refresh_token)

    return RefreshResponse(
        access_token=access_token,
        refresh_token=new_refresh_token
    )

@user_router.post("/logout", status_code=HTTP_200_OK)
async def logout(
    logout_request: TokenRefreshRequest,
    user_service: Annotated[UserService, Depends()],
):
    """
    로그아웃 API: `refresh_token`을 블랙리스트에 추가하여 폐기.
    """
    refresh_token = logout_request.refresh_token

    if refresh_token:
        await user_service.user_store.block_token(refresh_token, datetime.now(timezone.utc)) 

    return {"message": "로그아웃 완료"}

@user_router.get("/me", status_code=HTTP_200_OK)
async def me(user: Annotated[User, Depends(get_current_user_from_header)]) -> MyProfileResponse:
    """
    현재 로그인된 사용자의 프로필 정보를 반환.
    """
    return MyProfileResponse.from_user(user)

@user_router.patch("/me", status_code=HTTP_200_OK)
async def updateme(
    user: Annotated[User, Depends(get_current_user_from_header)], 
    user_update_request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends()],
) -> MyProfileResponse:
    return MyProfileResponse.from_user(await user_service.update_user(user_id=user.id, new_email=user_update_request.email, new_user_name=user_update_request.username, new_password=user_update_request.new_password))
