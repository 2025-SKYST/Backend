from typing import Annotated
from fastapi import File, UploadFile, Depends, HTTPException

from memory.app.image.dto.responses import URLResponse

from memory.app.image.store import ImageStore
from botocore.exceptions import ClientError

class ImageService:
    def __init__(
        self,
        image_store: Annotated[ImageStore, Depends()]
    ) : 
        self.image_store = image_store
    
    async def upload_image(
        self,
        s3_path : str,
        file: UploadFile = File(...)
    ) -> URLResponse :
        try:
            file_url = await self.image_store.upload_image_in_S3(s3_path, file)
        except ClientError as e:
            # e.response["Error"]["Code"] 등을 보고 세부 처리 가능
            raise HTTPException(500, detail="이미지 업로드에 실패했습니다.")
        return URLResponse.from_image_url(file_url)