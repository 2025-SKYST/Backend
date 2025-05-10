import aioboto3
import uuid
from functools import cache
from typing import Annotated, Sequence
from fastapi import File, UploadFile

from sqlalchemy import select, or_, and_, func, update, event
from memory.database.annotation import transactional
from memory.database.settings import AWSSettings
from memory.database.connection import SESSION

from memory.app.image.models import Image
from botocore.exceptions import ClientError

AWS_SETTINGS = AWSSettings()

class ImageStore:
    async def upload_image_in_S3(
        self, 
        s3_path : str,
        file: UploadFile = File(...)
    ) -> str : 
        # S3 는 별도의 session 을 이용해야 한다고 합니다.
        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region
        ) as s3_client:
            await s3_client.upload_fileobj(
                file.file,
                AWS_SETTINGS.s3_bucket,
                s3_path
            )
        
        file_url = f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/{s3_path}"

        return file_url