from mysol.common.errors import MysolHTTPException

class DraftNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "임시저장된 글을 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class NoAuthoriztionError(MysolHTTPException):
    def __init__(self, message: str = "비밀댓글입니다.") -> None:
        super().__init__(status_code=400, detail=message)
