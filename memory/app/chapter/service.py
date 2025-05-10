import jwt
from typing import Annotated, Optional
from fastapi import Depends
from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum

from memory.app.user.models import User
from memory.app.chapter.store import ChapterStore
from memory.app.user.hashing import Hasher
from mysol.database.settings import PW_SETTINGS

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class UserService:
    def __init__(self, chapter_store: Annotated[ChapterStore, Depends()]) -> None:
        self.chapter_store = chapter_store

    async def add_chapter(self, user_id: int, chapter_name: str) -> Chapter:

        chapter = await self.chapter_store.create(
            user_id=user_id,
            chapter_name=chapter_name
        )
