# memory/app/image/store.py

import aioboto3
from fastapi import File, UploadFile
from memory.database.settings import AWSSettings

AWS_SETTINGS = AWSSettings()

class ImageStore:
    async def upload_image_in_S3(
        self,
        s3_path: str,
        file: UploadFile = File(...)
    ) -> str:
        # 1) 바이트로 읽기
        body = await file.read()

        # 2) aioboto3 세션 열기
        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region,
        ) as s3_client:
            # 3) private 모드로 업로드
            await s3_client.put_object(
                Bucket=AWS_SETTINGS.s3_bucket,
                Key=s3_path,
                Body=body,
                ContentType=file.content_type,
                # ACL 옵션은 생략 → 기본 private
            )

            # 4) presigned URL 생성 (예: 1시간 유효)
            presigned_url = await s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": AWS_SETTINGS.s3_bucket,
                    "Key": s3_path
                },
                ExpiresIn=3600,  # 3600초 = 1시간
            )

        # 5) 호출자에게 presigned URL 반환
        return presigned_url
