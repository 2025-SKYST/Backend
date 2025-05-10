import uuid
import aioboto3

from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Depends
from botocore.exceptions import ClientError
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from memory.database.settings import AWS_SETTINGS
from memory.app.user.views import get_current_user_from_header
from memory.app.user.models import User
from memory.app.image.dto.responses import URLResponse

AWS_SETTINGS = AWS_SETTINGS()

image_router = APIRouter()

@image_router.post("/upload", status_code=201)
async def create_image(
    user: Annotated[User, Depends(get_current_user_from_header)],
    file: UploadFile = File(...)
) -> URLResponse:
    """
    사진 파일을 받아서 S3 서버에 업로드, URL을 반환
    """

    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    s3_path = f"uploads/{unique_filename}"

    return await image_service.upload_image(
        s3_path = s3_path,
        file = file
    )
