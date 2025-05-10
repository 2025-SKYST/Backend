from typing import Optional
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
