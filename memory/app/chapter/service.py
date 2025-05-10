import jwt
from typing import Annotated, Optional
from fastapi import Depends
from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum

from memory.app.chapter.models import Chapter
from memory.app.chapter.store import ChapterStore

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class ChapterService:
    def __init__(self, chapter_store: Annotated[ChapterStore, Depends()]) -> None:
        self.chapter_store = chapter_store

    async def add_chapter(self, user_id: int, chapter_name: str) -> Chapter:

        chapter = await self.chapter_store.add_chapter(
            user_id=user_id,
            chapter_name=chapter_name
        )

        return chapter
