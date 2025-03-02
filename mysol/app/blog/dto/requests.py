from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, field_validator, Field

from mysol.common.errors import InvalidFieldFormatError


class BlogCreateRequest(BaseModel):
    blog_name : str
    description : str
    
class BlogUpdateRequest(BaseModel):
    blog_name: str|None = None
    description: str|None = None
    main_image_URL: str|None = None
