from typing import Self
from pydantic import BaseModel


class URLResponse(BaseModel):
    file_url : str

    @staticmethod
    def from_image(file_url: str) -> "URLResponse":
        return URLResponse(
            file_url=file_url
        )