import uuid
import aioboto3

from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from botocore.exceptions import ClientError
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from memory.database.settings import AWSSettings
from memory.app.user.views import get_current_user_from_header
from memory.app.user.models import User
from memory.app.image.dto.responses import URLResponse, ImageProfileResponse
from memory.app.image.service import ImageService
from memory.app.chapter.service import ChapterService
from memory.database.connection import SESSION
from memory.common.openai_service import generate_continuous_story
from memory.app.image.models import Image
from memory.app.chapter.models import Chapter

AWS_SETTINGS = AWSSettings()

image_router = APIRouter()

@image_router.post("/upload", status_code=201)
async def upload_image(
    user: Annotated[User, Depends(get_current_user_from_header)],
    image_service: Annotated[ImageService, Depends()],
    file: UploadFile = File(...),
) -> URLResponse:
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    s3_path = f"uploads/{unique_filename}"

    return await image_service.upload_image(
        s3_path=s3_path,
        file=file
    )

@image_router.post("/create/{chapter_id}", status_code=201)
async def create_image(
    user: Annotated[User, Depends(get_current_user_from_header)],
    chapter_id: int,
    image_service: Annotated[ImageService, Depends()],
    chapter_service: Annotated[ChapterService, Depends()],
    file: UploadFile = File(...),
    query: Optional[str] = Form(None),
    keyword: Optional[str] = Form(None)
) -> ImageProfileResponse:
    
    chapter = await SESSION.get(Chapter, chapter_id)
    
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    s3_path = f"uploads/{unique_filename}"

    url_resp = await image_service.upload_image(
        s3_path=s3_path,
        file=file
    )
    file_url: str = url_resp.file_url

    await SESSION.refresh(chapter)
    previous_stories = [
        img.content
        for img in chapter.images
        if img.content is not None
    ]

    story_text = await generate_continuous_story(
        previous_stories=previous_stories,
        file_url = file_url,
        content_type=file.content_type,
        keywords=keyword,
        user_query=query,
    )
    
    image = Image(
        file_url = file_url,
        chapter_id = chapter_id,
        user_id = user.id,
        is_main = False,
        content = story_text,
    )

    SESSION.add(image)
    await SESSION.commit()

    return ImageProfileResponse.from_image(image)