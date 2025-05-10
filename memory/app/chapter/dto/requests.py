from pydantic import BaseModel

class ChapterCreateRequest(BaseModel):
    name: str
