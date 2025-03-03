from typing import Annotated, List, Optional
from pydantic import AfterValidator, BaseModel, field_validator, ValidationInfo
from mysol.app.article.errors import InvalidPasswordError
from mysol.common.errors import InvalidFieldFormatError
from mysol.app.image.dto.requests import ImageCreateRequest


def title_length_1_and_80(title: str | None) -> str | None:
    if title is None:
        return None  # None은 허용
    if len(title) < 1 or len(title) > 80:
        raise InvalidFieldFormatError("제목은 2자 이상 100자 이하로 작성해야 합니다.")
    return title


def title_not_empty(title: str | None) -> str | None:
    if title is None:
        return None  # None은 허용
    if title.strip() == "":
        raise InvalidFieldFormatError("제목은 공백만으로 구성될 수 없습니다.")
    return title

def content_min_valid_character(content: str | None) -> str | None:
    if content is None:
        return None  # None은 허용
    if len(content.strip()) == 0:
        raise InvalidFieldFormatError("내용에는 최소 1개의 문자(공백 제외)가 포함되어야 합니다.")
    return content

def password_valid(password: Optional[str], values: ValidationInfo) -> Optional[str]:
    protected = values.data.get("protected", 0)  # ✅ `.data.get()` 사용 (None 대비 default=0)
    if protected == 1 and (not password or len(password) < 1 or len(password) > 60):
        raise InvalidPasswordError
    return password

def validate_problem_numbers(problem_numbers: Optional[List[int]]) -> List[int]:
    """
    문제 번호 리스트 검증: 
    - 빈 리스트(`[]`)도 허용
    - 숫자로만 이루어져 있어야 함.
    """
    if problem_numbers is None:
        return []  # None이면 빈 리스트로 변환
    if not all(isinstance(num, int) and num > 0 for num in problem_numbers):
        raise InvalidFieldFormatError("문제 번호는 양의 정수여야 합니다.")
    return problem_numbers


class ArticleCreateRequest(BaseModel):
    title: Annotated[
        str | None,
        AfterValidator(title_length_1_and_80),
        AfterValidator(title_not_empty)
    ]
    content: Annotated[
        str | None,
        AfterValidator(content_min_valid_character)
    ]
    description: str
    main_image_url: Optional[str] = None
    category_id: int
    secret: int
    protected: int
    password: Optional[str] = None
    images: List[ImageCreateRequest] = []
    comments_enabled: int = 1  # 1 = 활성화, 0 = 비활성화
    problem_numbers: List[int] = []  # ✅ 기본값을 빈 리스트로 설정

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: Optional[str], values: ValidationInfo):
        return password_valid(password, values)

    @field_validator("problem_numbers")
    @classmethod
    def validate_problem_numbers(cls, problem_numbers: Optional[List[int]]):
        return validate_problem_numbers(problem_numbers)


class ArticleUpdateRequest(BaseModel):
    title: Annotated[
        Optional[str],
        AfterValidator(title_length_1_and_80),
        AfterValidator(title_not_empty)
    ] = None
    content: Annotated[
        Optional[str],
        AfterValidator(content_min_valid_character)
    ] = None
    description: Optional[str] = None
    main_image_url: Optional[str] = None
    category_id: Optional[int] = None
    secret: Optional[int] = None
    protected: Optional[int] = None
    password: Optional[str] = None
    images: List[ImageCreateRequest] = []
    comments_enabled: Optional[int] = None  # 사용자가 수정할 수 있도록 설정
    problem_numbers: List[int] = []  # ✅ 기본값을 빈 리스트로 설정

    @field_validator("password", mode="before")
    def validate_password(cls, password, values):
        return password_valid(password, values)

    @field_validator("problem_numbers")
    @classmethod
    def validate_problem_numbers(cls, problem_numbers: Optional[List[int]]):
        return validate_problem_numbers(problem_numbers)
