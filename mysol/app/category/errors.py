from mysol.common.errors import MysolHTTPException

class BlogNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "블로그를 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class CategoryNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "카테고리를 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class CategoryNameDuplicateError(MysolHTTPException):
    def __init__(self, message: str = "중복되는 카테고리 이름이 존재합니다.") -> None:
        super().__init__(status_code=400, detail=message)

class InvalidFieldFormatError(MysolHTTPException):
    def __init__(self, message: str = "올바르지 않은 필드 형식입니다.") -> None:
        super().__init__(status_code=400, detail=message)

class MissingRequiredFieldError(MysolHTTPException):
    def __init__(self, message: str = "필수 항목 중 빠진 것이 있습니다.") -> None:
        super().__init__(status_code=400, detail=message)

class NotOwnerError(MysolHTTPException):
    def __init__(self, message: str = "블로그의 주인이 아닙니다.") -> None:
        super().__init__(status_code=401, detail=message)