import uuid
import aioboto3

from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Depends
from botocore.exceptions import ClientError
from typing import Annotated

from mysol.database.settings import AWSSettings
from mysol.app.user.models import User
from mysol.app.user.views import get_current_user_from_header
from mysol.app.image.dto.responses import ImageDetailResponse
from mysol.app.image.service import ImageService
from mysol.app.image.dto.requests import PresignedUrlRequest
from botocore.exceptions import BotoCoreError, ClientError
# AWS 설정 불러오기
AWS_SETTINGS = AWSSettings()

image_router = APIRouter()

@image_router.post("/upload/", status_code = 201)
async def upload_image(
    user: Annotated[User, Depends(get_current_user_from_header)],
    image_service: Annotated[ImageService, Depends()],
    file: UploadFile = File(...)
) -> ImageDetailResponse :
    unique_filename = f"{uuid.uuid4()}-{file.filename}"

        # S3 업로드 경로
    s3_path = f"uploads/{unique_filename}"
    
    return await image_service.upload_image(
        s3_path = s3_path,
        file = file
    )

@image_router.delete("/deletes/", status_code = 201)
async def delete_image(
    user: Annotated[User, Depends(get_current_user_from_header)],
    image_service: Annotated[ImageService, Depends()],
    file_url: str
) -> dict :
    return await image_service.delete_image(file_url)

    
@image_router.post("/generate-presigned-urls", status_code=201)
async def generate_presigned_urls(
    user: Annotated[User, Depends(get_current_user_from_header)],
    image_service: Annotated[ImageService, Depends()],
    request: PresignedUrlRequest
) :
    return await image_service.generate_presigned_url(
        request = request
    )