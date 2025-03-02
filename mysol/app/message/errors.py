from mysol.common.errors import MysolHTTPException

class MessageNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "쪽지를 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class UnauthorizedMessageAccessError(MysolHTTPException):
    def __init__(self, message: str = "허가되지 않은 접근입니다.") -> None:
        super().__init__(status_code=403, detail=message)

