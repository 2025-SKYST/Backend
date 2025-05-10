from typing import Optional
from sqlalchemy import select
from datetime import datetime

from memory.app.user.models import User, BlockedToken
from mysol.database.annotation import transactional
from mysol.database.connection import SESSION
from memory.app.user.hashing import Hasher
from memory.app.user.errors import UserNameAlreadyExistsError

class UserStore:
    @transactional
    async def add_user(self, username: str, login_id: str, password: str, birth: datetime) -> User:
        user = User(
            username=username,
            login_id=login_id,
            password=password,
            birth=birth
        )
        SESSION.add(user)
        await SESSION.flush()
        return user

    async def get_user_by_field(self, field: str, value) -> Optional[User]:
        return await SESSION.scalar(select(User).where(getattr(User, field) == value))

    # @transactional
    # async def update_user(
    #     self, user_id: int, username: Optional[str], email: Optional[str], new_password: Optional[str]
    # ) -> User:
    #     user= await self.get_user_by_id(user_id)

    #     if username:
    #         if await self.get_user_by_username(username=username):
    #             raise UserNameAlreadyExistsError()
    #         user.username = username
    #     if email:
    #         user.email = email
    #     if new_password:
    #         user.password = new_password
    #     SESSION.merge(user)
    #     await SESSION.flush()
    #     await SESSION.refresh(user)


    #     return user

    @transactional
    async def block_token(self, token_id: str, expired_at: datetime) -> None:
        blocked_token = BlockedToken(token_id=token_id, expired_at=expired_at)
        SESSION.add(blocked_token)

    async def is_token_blocked(self, token_id: str) -> bool:
        return (
            await SESSION.scalar(
                select(BlockedToken).where(BlockedToken.token_id == token_id)
            )
            is not None
        )
