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

@image_router.post("/create/{chapter_id}, status_code=201")
async def create_image(
    user: Annotated[User, Depends(get_current_user_from_header)],
    chapter_id: int,
    image_service: Annotated[ImageService, Depends()],
    file: UploadFile = File(...),
    query: Optional[str] = Form(None),
    keyword: Optional[str] = Form(None)
) -> ImageProfileResponse:
    
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    s3_path = f"uploads/{unique_filename}"


