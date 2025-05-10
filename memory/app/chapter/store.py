from typing import Optional,List
from sqlalchemy import select
from datetime import datetime

from memory.app.user.models import User
from memory.database.annotation import transactional
from memory.database.connection import SESSION
from memory.app.chapter.models import Chapter

class ChapterStore:
    @transactional
    async def add_chapter(
        self, user_id: int, chapter_name: str,
    ) -> Chapter:
        new_chapter = Chapter(
            chapter_name=chapter_name,
            user_id=user_id,
        )
        SESSION.add(new_chapter)
        await SESSION.flush()
        return new_chapter
    
    @transactional
    async def get_chapters(
        self,
        user_id: int,
    ) -> List[Chapter]:
        """
        해당 user_id 가 가진 모든 Chapter 를 조회하여 리스트로 반환합니다.
        """
        stmt = select(Chapter).where(Chapter.user_id == user_id)
        result = await SESSION.execute(stmt)
        return result.scalars().all()