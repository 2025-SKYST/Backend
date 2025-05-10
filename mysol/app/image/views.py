from fastapi import APIRouter, Depends, Response, Request, HTTPException
from typing import Annotated, Optional
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mysol.app.user.dto.requests import UserSignupRequest, UserSigninRequest, TokenRefreshRequest, UserUpdateRequest
from mysol.app.user.dto.reponses import UserSignupResponse, UserSigninResponse, MyProfileResponse, RefreshResponse
from mysol.app.user.service import UserService
from mysol.app.user.models import User
from mysol.app.user.errors import InvalidTokenError, MissingAccessTokenError
from datetime import datetime, timezone

import uuid
import aioboto3

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError, BotoCoreError
from typing import Annotated

from mysol.database.settings import AWSSettings, SessionLocal
from mysol.app.user.models import User
from mysol.app.user.views import get_current_user_from_header
from mysol.app.image.models import Image, Description
from mysol.app.chapter.models import Chapter

AWS_SETTINGS = AWSSettings()
image_router = APIRouter(prefix="/api/images")


@image_router.post("/create_image/{chapter_id}", status_code=201)
async def create_image(
    chapter_id: int,
    user: Annotated[User, Depends(get_current_user_from_header)],
    file: UploadFile = File(...),
) -> dict:
    """
    1. S3에 업로드
    2. Image 테이블에 row 생성
    3. Chapter.image_id 리스트에 방금 생성된 image.id 추가
    4. pseudo 코드로 이미지→텍스트 변환 후 Description 테이블에 저장
    5. image.id 반환
    """
    # 1) 파일명 생성 및 S3 경로
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    s3_key = f"uploads/{unique_filename}"

    # 2) S3 업로드 및 presigned URL 생성
    session = aioboto3.Session()
    async with session.client(
        "s3",
        aws_access_key_id=AWS_SETTINGS.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SETTINGS.AWS_SECRET_ACCESS_KEY,
        region_name=AWS_SETTINGS.AWS_REGION,
    ) as s3_client:
        try:
            await s3_client.upload_fileobj(file.file, AWS_SETTINGS.S3_BUCKET_NAME, s3_key)
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": AWS_SETTINGS.S3_BUCKET_NAME, "Key": s3_key},
                ExpiresIn=3600,
            )
        except (ClientError, BotoCoreError) as e:
            raise HTTPException(status_code=500, detail="S3 업로드 또는 URL 생성 실패") from e

    # 3) DB에 Image, Chapter, Description 업데이트
    db: Session = SessionLocal()
    try:
        # Image row 생성
        image = Image(image_url=presigned_url, chapter_id=chapter_id)
        db.add(image)
        db.flush()  # image.id 확보

        # Chapter.image_id 리스트에 추가
        chapter = db.query(Chapter).get(chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="해당 챕터 없음")
        chapter.image_id.append(image.id)

        # pseudo code: 이미지 → 텍스트 변환
        # converted_text = convert_image_to_text(presigned_url)
        converted_text = pseudo_convert_image_to_text(presigned_url)

        # Description row 생성
        description = Description(image_id=image.id, story=converted_text)
        db.add(description)

        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB 저장 중 오류") from e
    finally:
        db.close()

    return {"image_id": image.id}


@image_router.get("/get_image_description/{image_id}", status_code=200)
async def get_image_description(
    image_id: int,
    user: Annotated[User, Depends(get_current_user_from_header)],
) -> dict:
    """
    image_id에 대응하는 Description.story 반환
    """
    db: Session = SessionLocal()
    try:
        desc = db.query(Description).filter(Description.image_id == image_id).first()
        if not desc:
            raise HTTPException(status_code=404, detail="Description 없음")
        return {"story": desc.story}
    finally:
        db.close()
