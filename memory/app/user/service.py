import jwt
from typing import Annotated, Optional
from fastapi import Depends
from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum

from memory.app.user.models import User
from memory.app.user.store import UserStore
from memory.app.user.hashing import Hasher
from mysol.database.settings import PW_SETTINGS

from memory.app.user.errors import UserNameAlreadyExistsError, LoginIdAlreadyExistsError, UserUnsignedError, UserNotFoundError, InvalidPasswordError, InvalidTokenError, ExpiredSignatureError, BlockedTokenError

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()]) -> None:
        self.user_store = user_store

    async def add_user(self, username: str, login_id: str, password: str, birth: datetime) -> User:
        # 중복 검사
        if await self.user_store.get_user_by_field("username", username):
            raise UserNameAlreadyExistsError("이미 사용 중인 사용자 이름입니다.")
        if await self.user_store.get_user_by_field("login_id", login_id):
            raise LoginIdAlreadyExistsError("이미 사용 중인 로그인 ID입니다.")

        hashed_password = Hasher.hash_password(password)

        user = await self.user_store.add_user(
            username=username,
            login_id=login_id,
            password=hashed_password,
            birth=birth
        )

        return user

    async def get_user_by_login_id(self, login_id: str) -> User:
        return await self.user_store.get_user_by_field("login_id", login_id)

    async def signin(self, login_id: str, password: str) -> tuple[str, str]:
        user = await self.get_user_by_login_id(login_id=login_id)

        if not user:
            raise UserNotFoundError()
        
        if not Hasher.verify_password(password, user.password):
            raise InvalidPasswordError()
        
        return self.issue_tokens(user.login_id)
    
    # async def update_user(
    #     self,
    #     user_id : int,
    #     new_user_name: str|None,
    #     new_email: str|None,
    #     new_password: str|None,
    # ) -> User:
    #     user = await self.user_store.update_user(user_id=user_id, username=new_user_name, email=new_email, new_password=new_password)
    #     return user

    def issue_tokens(self, login_id: str) -> tuple[str, str]:
        """
        JWT 토큰 발급:
        - access_token: 5분 만료
        - refresh_token: 3시간 만료
        """
        now = datetime.utcnow()

        access_payload = {
            "sub": login_id,
            "exp": now + timedelta(minutes=5),
            "typ": TokenType.ACCESS.value,
            "iat": now
        }
        access_token = jwt.encode(access_payload, PW_SETTINGS.secret_for_jwt, algorithm="HS256")

        refresh_payload = {
            "sub": login_id,
            "jti": uuid4().hex,
            "exp": now + timedelta(hours=3),
            "iat": now,
            "typ": TokenType.REFRESH.value
        }
        refresh_token = jwt.encode(refresh_payload, PW_SETTINGS.secret_for_jwt, algorithm="HS256")

        return access_token, refresh_token

    def validate_access_token(self, token: str) -> str:
        """
        access_token을 검증하고, 사용자 login_id를 반환합니다.
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

            return payload["sub"]  # now returns login_id

        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def validate_refresh_token(self, token: str) -> str:
        """
        refresh_token을 검증하고, 사용자 login_id를 반환합니다.
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

        return payload["sub"]  # login_id
    
    async def reissue_tokens(self, refresh_token: str) -> tuple[str, str]:
        """
        refresh_token을 검증하고, 새로운 access_token과 refresh_token을 발급합니다.
        """
        login_id = await self.validate_refresh_token(refresh_token)

        await self.user_store.block_token(refresh_token, datetime.utcnow())

        return self.issue_tokens(login_id)
