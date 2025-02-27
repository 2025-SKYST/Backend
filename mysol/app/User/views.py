from fastapi import APIRouter, Depends, Response, Request, HTTPException, Cookie
from typing import Annotated
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mysol.app.User.dto.requests import UserSignupRequest, UserSigninRequest
from mysol.app.User.dto.reponses import UserSignupResponse, UserSigninResponse, MyProfileResponse, RefreshResponse
from mysol.app.User.service import UserService
from mysol.app.User.models import User
from mysol.app.User.errors import InvalidTokenError, MissingAccessTokenError
from datetime import datetime

user_router = APIRouter()
security = HTTPBearer()

async def get_current_user_from_cookie(
    user_service: Annotated[UserService, Depends()],
    access_token: str = Cookie(None)  # ✅ 쿠키에서 Access Token 가져오기
) -> User:
    """
    `httpOnly` 쿠키의 `access_token`을 검증하여 사용자 정보를 가져옴.
    """
    if not access_token:
        raise MissingAccessTokenError()

    email = user_service.validate_access_token(access_token)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise InvalidTokenError()
    
    return user

@user_router.post("/signup", response_model=UserSignupResponse, status_code=HTTP_201_CREATED)
async def signup(
    signup_request: UserSignupRequest,
    user_service: Annotated[UserService, Depends()]
) -> UserSignupResponse:
    """
    새로운 사용자를 등록하는 API.
    """
    user = await user_service.add_user(
        email=signup_request.email,
        username=signup_request.username,
        password=signup_request.password
    )
    return UserSignupResponse(email=user.email, username=user.username)

@user_router.post("/signin", status_code=HTTP_200_OK)
async def signin(
    response: Response,
    user_service: Annotated[UserService, Depends()],
    signin_request: UserSigninRequest,
):
    """
    로그인 API: access_token 및 refresh_token 발급.
    `refresh_token`을 `httpOnly` 쿠키에 저장.
    """
    access_token, refresh_token = await user_service.signin(
        signin_request.email, signin_request.password
    )
    user = await user_service.get_user_by_email(signin_request.email)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # JavaScript에서 접근 불가능 (XSS 방지)
        secure=True,  # HTTPS에서만 사용 가능
        samesite="Lax",  # CSRF 방지
        max_age=60 * 10  # 10분 유지
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # JavaScript에서 접근 불가능 (XSS 방지)
        secure=True,  # HTTPS에서만 사용 가능 (보안 강화)
        samesite="Lax",  # CSRF 방지
        max_age=60 * 60 * 3  # ✅ 1일 유지 (보안 강화)
    )

    return UserSigninResponse(username=user.username)

@user_router.post("/refresh", status_code=HTTP_200_OK)
async def refresh(
    request: Request,
    response: Response,
    user_service: Annotated[UserService, Depends()],
) -> RefreshResponse:
    """
    `refresh_token`을 이용해 `access_token`을 재발급하는 API.
    기존 `refresh_token`을 블랙리스트에 추가하여 재사용 방지.
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    
    access_token, new_refresh_token = await user_service.reissue_tokens(refresh_token)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=60 * 10  # 10분 유지
    )

    # ✅ 새 refresh_token을 다시 쿠키에 저장
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=60 * 60 * 3  # ✅ 1일 유지 (보안 강화)
    )

    return RefreshResponse()

@user_router.post("/logout", status_code=HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    user_service: Annotated[UserService, Depends()],
):
    """
    로그아웃 API: `refresh_token`을 블랙리스트에 추가 후 쿠키에서 삭제.
    """
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await user_service.user_store.block_token(refresh_token, datetime.utcnow())  # ✅ refresh_token 차단

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")  # ✅ 쿠키에서 refresh_token 삭제
    return {"message": "로그아웃 완료"}

@user_router.get("/me", status_code=HTTP_200_OK)
async def me(user: Annotated[User, Depends(get_current_user_from_cookie)]) -> MyProfileResponse:
    """
    현재 로그인된 사용자의 프로필 정보를 반환.
    """
    return MyProfileResponse.from_user(user)
