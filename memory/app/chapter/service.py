import jwt
from typing import Annotated, List
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum

from memory.app.chapter.models import Chapter
from memory.app.chapter.store import ChapterStore
from memory.app.chapter.dto.reponses import ChapterProfileResponse

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class ChapterService:
    def __init__(self, chapter_store: Annotated[ChapterStore, Depends()]) -> None:
        self.chapter_store = chapter_store

    async def add_chapter(self, user_id: int, chapter_name: str) -> ChapterProfileResponse:

        chapter = await self.chapter_store.add_chapter(
            user_id=user_id,
            chapter_name=chapter_name
        )

        return ChapterProfileResponse.from_chapter(chapter)
    
    async def get_chapters(self, user_id: int) -> List[Chapter]:
        """
        주어진 user_id가 가진 모든 Chapter를 조회하여 반환합니다.
        """
        chapters = await self.chapter_store.get_chapters(user_id=user_id)
        return chapters
    
    async def get_chapter_by_id(
        self,
        chapter_id: int,
    ) -> Chapter:
        """
        주어진 ID에 해당하는 Chapter를 조회한 뒤, 없으면 404 에러를 발생시킵니다.
        """
        chapter = await self.chapter_store.get_chapter_by_id(chapter_id=chapter_id)
        if chapter is None:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return chapter
