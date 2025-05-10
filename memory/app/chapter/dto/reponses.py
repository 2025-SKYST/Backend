from pydantic import BaseModel
from typing import List, Optional
from memory.app.chapter.models import Chapter
from memory.app.image.dto.responses import ImageProfileResponse

class ChapterProfileResponse(BaseModel):
    id: int
    chapter_name: str
    prologue: Optional[str] = None
    epilogue: Optional[str] = None
    main_image_url: Optional[str] = None  # 대표 이미지 URL

    @staticmethod
    def from_chapter(chapter: Chapter) -> "ChapterProfileResponse":
        # images 관계에서 첫 번째 URL을 우선 사용
        first_url = chapter.images[0].file_url if chapter.images else None
        return ChapterProfileResponse(
            id=chapter.id,
            chapter_name=chapter.chapter_name,
            prologue=chapter.prologue,
            epilogue=chapter.epilogue,
            main_image_url=first_url,
        )

class ChapterListResponse(BaseModel):
    chapters: List[ChapterProfileResponse]

    @staticmethod
    def from_chapters(chapters: List[Chapter]) -> "ChapterListResponse":
        return ChapterListResponse(
            chapters=[ChapterProfileResponse.from_chapter(ch) for ch in chapters]
        )
    
class ChapterDetailResponse(BaseModel):
    id: int
    chapter_name: str
    prologue: Optional[str] = None
    epilogue: Optional[str] = None
    main_image_url: Optional[str] = None   
    images: List[ImageProfileResponse] = []

    @staticmethod
    def from_chapter(chapter: Chapter) -> "ChapterDetailResponse":
        return ChapterDetailResponse(
            id=chapter.id,
            chapter_name=chapter.chapter_name,
            prologue=chapter.prologue,
            epilogue=chapter.epilogue,
            main_image_url=chapter.main_image_url,
            images=[ImageProfileResponse.from_image(img) for img in chapter.images],
        )
