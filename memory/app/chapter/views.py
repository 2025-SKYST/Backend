from fastapi import APIRouter, HTTPException, Path, Body, Depends
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from mysol.database.settings import get_db
from memory.app.chapter.models import Chapter
from memory.app.user.models import User
from memory.app.chapter.dto.requests import ChapterCreateRequest
from memory.app.user.views import get_current_user_from_header

chapter_router = APIRouter()

@chapter_router.get("/create", status_code=201)
async def create_chapter(
    user: Annotated[User, Depends(get_current_user_from_header)],
    request: ChapterCreateRequest,
) -> int:
    """
    chapter를 생성
    """
