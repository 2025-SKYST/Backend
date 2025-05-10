from fastapi import APIRouter, HTTPException, Path, Body, Depends
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from mysol.database.settings import get_db
from memory.app.chapter.models import Chapter

image_router = APIRouter()

class ChapterCreateRequest(BaseModel):
    name: str

@image_router.post("/create_chapter/{id}", status_code=201)
async def create_chapter(
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int = Path(..., description="생성할 챕터의 ID"),
    request: ChapterCreateRequest = Body(..., description="생성할 챕터의 이름"),
) -> dict:
    """
    - id: 챕터 테이블의 PK로 사용할 정수 ID
    - request.name: 새로 생성할 챕터의 name 필드
    """
    new_chapter = Chapter(id=id, name=request.name)
    db.add(new_chapter)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="챕터 생성에 실패했습니다.")
    return {"success": True}

@image_router.get("/get_image/{id}", status_code=200)
async def get_image(
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int = Path(..., description="조회할 이미지의 ID"),
) -> dict:
    """
    - id: image 테이블의 PK에 해당하는 ID
    - 성공 시 해당 row의 image 필드를 리턴
    """
    image_obj = await db.get(Image, id)
    if not image_obj:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
    return {"image": image_obj.image}
