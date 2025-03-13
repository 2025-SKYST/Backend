import jwt
from typing import Annotated, Optional
from fastapi import Depends
from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum

from mysol.app.user.models import User
from mysol.app.user.store import UserStore
from mysol.app.user.hashing import Hasher
from mysol.database.settings import PW_SETTINGS
from mysol.app.blog.service import BlogService
from mysol.app.user.errors import (
    EmailAlreadyExistsError,
    UserNameAlreadyExistsError,
    InvalidPasswordError,
    UserUnsignedError,
    UserNotFoundError,
    ExpiredSignatureError,
    InvalidTokenError,
    BlockedTokenError
)

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()], blog_service: Annotated[BlogService, Depends()]) -> None:
        self.user_store = user_store
        self.blog_service = blog_service

    async def add_user(self, email: str, password: str, username: str) -> User:
        if await self.user_store.get_user_by_field("email", email):
            raise EmailAlreadyExistsError("이미 사용 중인 이메일입니다.")
        if await self.user_store.get_user_by_field("username", username):
            raise UserNameAlreadyExistsError("이미 사용 중인 사용자 이름입니다.")
        
        blogname = f"{username}님의 블로그"
        blogdescription = f"{username}님의 블로그입니다."    

        hashed_password = Hasher.hash_password(password)
        user = await self.user_store.add_user(email=email, password=hashed_password, username=username)    
        
        await self.blog_service.create_blog(user_id=user.id, blog_name=blogname, description=blogdescription)
        
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_store.get_user_by_email(email)
        if not user:
            raise UserUnsignedError("존재하지 않는 사용자입니다.")
        return user

    async def signin(self, email: str, password: str) -> tuple[str, str]:
        user = await self.get_user_by_email(email)

        if not user:
            raise UserNotFoundError()
    
        if not Hasher.verify_password(password, user.password):
            raise InvalidPasswordError()
        
        return self.issue_tokens(user.email)
    
    async def update_user(
        self,
        user_id : int,
        new_user_name: str|None,
        new_email: str|None,
        new_password: str|None,
    ) -> User:
        user = await self.user_store.update_user(user_id=user_id, username=new_user_name, email=new_email, new_password=new_password)
        return user

    def issue_tokens(self, email: str) -> tuple[str, str]:
        """
        보안 강화 설정 적용:
        - access_token 만료: 5분
        - refresh_token 만료: 1일
        - refresh_token이 24시간 동안 사용되지 않으면 만료
        """
        now = datetime.utcnow()

        access_payload = {
            "sub": email,
            "exp": now + timedelta(minutes=5),
            "typ": TokenType.ACCESS.value,
            "iat": now
        }
        access_token = jwt.encode(access_payload, PW_SETTINGS.secret_for_jwt, algorithm="HS256")

        refresh_payload = {
            "sub": email,
            "jti": uuid4().hex,
            "exp": now + timedelta(hours=3),
            "iat": now,
            "typ": TokenType.REFRESH.value,
        }
        refresh_token = jwt.encode(refresh_payload, PW_SETTINGS.secret_for_jwt, algorithm="HS256")

        return access_token, refresh_token

    def validate_access_token(self, token: str) -> str:
        """
        access_token을 검증하고, 사용자 이메일을 반환합니다.
        """
        try:
            payload = jwt.decode(
                token,
                PW_SETTINGS.secret_for_jwt,
                algorithms=["HS256"],
                options={"require": ["sub", "exp", "iat"]}
            )
            if payload["typ"] != TokenType.ACCESS.value:
                raise InvalidTokenError()
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def validate_refresh_token(self, token: str) -> str:
        """
        refresh_token을 검증하고, 사용자 이메일을 반환합니다.
        """
        try:
            payload = jwt.decode(
                token,
                PW_SETTINGS.secret_for_jwt,
                algorithms=["HS256"],
                options={"require": ["sub", "exp", "iat", "jti"]}
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

        if payload["typ"] != TokenType.REFRESH.value:
            raise InvalidTokenError()

        if await self.user_store.is_token_blocked(payload["jti"]):
            raise BlockedTokenError()

        return payload["sub"]

    async def reissue_tokens(self, refresh_token: str) -> tuple[str, str]:
        """
        refresh_token을 검증하고, 새로운 access_token과 refresh_token을 발급합니다.
        """
        username = await self.validate_refresh_token(refresh_token)

        await self.user_store.block_token(refresh_token, datetime.utcnow())

        return self.issue_tokens(username)
