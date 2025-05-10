import re
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator
from typing import Annotated, Optional
from datetime import datetime

from mysol.common.errors import InvalidFieldFormatError

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

USERNAME_ERROR_MSG = "아이디는 3~20자의 영문 대소문자, 숫자, `_`, `-`만 사용할 수 있습니다."
PASSWORD_LENGTH_ERROR_MSG = "비밀번호는 8자 이상 20자 이하로 설정해야 합니다."
PASSWORD_COMPLEXITY_ERROR_MSG = "비밀번호는 영어 대문자, 영어 소문자, 숫자, 특수문자 중 최소 2가지 이상을 포함해야 합니다."

def validate_username(value: str) -> str:
    if not re.fullmatch(USERNAME_PATTERN, value):
        raise InvalidFieldFormatError(USERNAME_ERROR_MSG)
    return value

def validate_password(value: str) -> str:
    if len(value) < 8 or len(value) > 20:
        raise InvalidFieldFormatError(PASSWORD_LENGTH_ERROR_MSG)

    contains_uppercase = any(c.isupper() for c in value)
    contains_lowercase = any(c.islower() for c in value)
    contains_digit = any(c.isdigit() for c in value)
    contains_special = any(not c.isalnum() for c in value)

    if (contains_uppercase + contains_lowercase + contains_digit + contains_special) < 2:
        raise InvalidFieldFormatError(PASSWORD_COMPLEXITY_ERROR_MSG)

    return value

class UserSignupRequest(BaseModel):
    username: Annotated[str, AfterValidator(validate_username)]
    login_id: str
    password: Annotated[str, AfterValidator(validate_password)]
    birth_year: int
    birth_month: int
    birth_date: int
    birth_hour: int
    birth_minute: int

    def to_birth_datetime(self) -> datetime:
        """입력된 년/월/일/시/분 정보를 datetime으로 변환합니다."""
        try:
            return datetime(
                self.birth_year,
                self.birth_month,
                self.birth_date,
                self.birth_hour,
                self.birth_minute
            )
        except ValueError as e:
            raise ValueError(f"유효하지 않은 생년월일 정보입니다: {e}")

class UserSigninRequest(BaseModel):
    login_id: str
    password: str

class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    new_password: Optional[str] = None

class UserSigninRequest(BaseModel):
    email: EmailStr
    password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str