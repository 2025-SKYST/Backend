from mysol.common.errors import MysolHTTPException

class BlognameAlreadyExistsError(MysolHTTPException):
    def __init__(self, message: str = "이미 존재하는 블로그 이름입니다.") -> None:
        super().__init__(status_code=400, detail=message)

class NotificationNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "알림을 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class InvalidFieldFormatError(MysolHTTPException):
    def __init__(self, message: str = "올바르지 않은 필드 형식입니다.") -> None:
        super().__init__(status_code=400, detail=message)

class MissingRequiredFieldError(MysolHTTPException):
    def __init__(self, message: str = "필수 항목 중 빠진 것이 있습니다.") -> None:
        super().__init__(status_code=400, detail=message)

class UserUnsignedError(MysolHTTPException):
    def __init__(self, message: str = "유저가 로그인하지 않았습니다.") -> None:
        super().__init__(status_code=404, detail=message)