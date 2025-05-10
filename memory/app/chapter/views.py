from fastapi import APIRouter, HTTPException, Path, Body, Depends
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from memory.app.chapter.models import Chapter
from memory.app.chapter.service import ChapterService
from memory.app.user.models import User
from memory.app.chapter.dto.requests import ChapterCreateRequest
from memory.app.chapter.dto.reponses import ChapterProfileResponse, ChapterListResponse, ChapterDetailResponse
from memory.app.user.views import get_current_user_from_header

chapter_router = APIRouter()

@chapter_router.post("/create", status_code=201)
async def create_chapter(
    user: Annotated[User, Depends(get_current_user_from_header)],
    request: ChapterCreateRequest,
    chapter_service: Annotated[ChapterService, Depends()]
) -> ChapterProfileResponse:
    """
    chapter를 생성
    """
    chapter = await chapter_service.add_chapter(user_id=user.id, chapter_name=request.name)
    
    return ChapterProfileResponse.from_chapter(chapter)

@chapter_router.get("/get", status_code=201)
async def get_my_chapters(
    user: Annotated[User, Depends(get_current_user_from_header)],
    chapter_service: Annotated[ChapterService, Depends()],
) -> ChapterListResponse:
    """
    현재 유저가 가진 모든 chapter 리스트를 반환
    """
    chapters = await chapter_service.get_chapters(user_id=user.id)
    return ChapterListResponse.from_chapters(chapters)

@chapter_router.get("/get/{chapter_id}", status_code=201)
async def get_chapter_by_id(
    user: Annotated[User, Depends(get_current_user_from_header)],
    chapter_service: Annotated[ChapterService, Depends()],
    chapter_id: int
) -> ChapterDetailResponse:
    """
    단일 chapter의 상세 정보 (메타데이터+이미지 리스트)를 반환합니다.
    """
    chapter = await chapter_service.get_chapter(
        user_id=user.id,
        chapter_id=chapter_id,
    )
    return ChapterDetailResponse.from_chapter(chapter)