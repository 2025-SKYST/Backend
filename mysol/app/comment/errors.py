from mysol.common.errors import MysolHTTPException

class BlogNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "블로그를 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class CommentNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "댓글을 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class ParentOtherSectionError(MysolHTTPException):
    def __init__(self, message: str = "parent와 children 위치가 다릅니다") -> None:
        super().__init__(status_code=404, detail=message)

class InvalidFieldFormatError(MysolHTTPException):
    def __init__(self, message: str = "올바르지 않은 필드 형식입니다.") -> None:
        super().__init__(status_code=400, detail=message)

class MissingRequiredFieldError(MysolHTTPException):
    def __init__(self, message: str = "필수 항목 중 빠진 것이 있습니다.") -> None:
        super().__init__(status_code=400, detail=message)

class InvalidLevelError(MysolHTTPException):
    def __init__(self, message: str = "부모 레벨은 1이어야 합니다.") -> None:
        super().__init__(status_code=404, detail=message)

class NotOwnerError(MysolHTTPException):
    def __init__(self, message: str = "블로그의 주인이 아닙니다.") -> None:
        super().__init__(status_code=401, detail=message)

class UserHasNoBlogError(MysolHTTPException):
    def __init__(self, message: str = "유저가 블로그를 소유하고 있지 않습니다.") -> None:
        super().__init__(status_code=404, detail=message)