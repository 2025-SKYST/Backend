from pydantic import BaseModel
from typing import List, Optional
from memory.app.chapter.models import Chapter
from memory.app.image.dto.responses import ImageProfileResponse

class ChapterProfileResponse(BaseModel):
    id: int
    chapter_name: str
    prologue: Optional[str] = None
    epilogue: Optional[str] = None


    @staticmethod
    def from_chapter(chapter: Chapter) -> "ChapterProfileResponse":
        return ChapterProfileResponse(
            id=chapter.id,
            chapter_name=chapter.chapter_name,
            prologue=chapter.prologue,
            epilogue=chapter.epilogue,
        )

class ChapterListResponse(BaseModel):
    chapters: List[ChapterProfileResponse]

    @staticmethod
    def from_chapters(chapters: list[Chapter]) -> "ChapterListResponse":
        return ChapterListResponse(
            chapters=[ChapterProfileResponse.from_chapter(ch) for ch in chapters]
        )
    
class ChapterDetailResponse(BaseModel):
    id: int
    chapter_name: str
    prologue: Optional[str] = None
    epilogue: Optional[str] = None
    images: List[ImageProfileResponse] = []

    @staticmethod
    def from_chapter(chapter: Chapter) -> "ChapterDetailResponse":
        return ChapterDetailResponse(
            id=chapter.id,
            chapter_name=chapter.chapter_name,
            prologue=chapter.prologue,
            epilogue=chapter.epilogue,
            images=[ImageProfileResponse.from_image(img) for img in chapter.images],
        )