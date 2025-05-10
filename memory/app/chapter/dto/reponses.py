from pydantic import BaseModel

from memory.app.chapter.models import Chapter

class ChapterProfileResponse(BaseModel):
    id: int
    chapter_name: str
    prologue: str
    epilogue: str

    @staticmethod
    def from_chapter(chapter: Chapter) -> "ChapterProfileResponse":
        return ChapterProfileResponse(
            id=chapter.id,
            chapter_name=chapter.chapter_name,
            prologue=chapter.prologue,
            epilogue=chapter.epilogue,
        )
    