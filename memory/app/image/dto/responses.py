from typing import Self
from pydantic import BaseModel
from typing import Optional

from memory.app.image.models import Image

class URLResponse(BaseModel):
    file_url : str

    @staticmethod
    def from_image(file_url: str) -> "URLResponse":
        return URLResponse(
            file_url=file_url
        )
    
class ImageProfileResponse(BaseModel):
    id: int
    file_url: str
    chapter_id: Optional[int] = None
    user_id: Optional[int] = None
    is_main: bool
    content: Optional[str] = None

    @staticmethod
    def from_image(image: Image) -> "ImageProfileResponse":
        return ImageProfileResponse(
            id=image.id,
            file_url=image.file_url,
            chapter_id=image.chapter_id,
            user_id=image.user_id,
            is_main=image.is_main,
            content=image.content,
        )