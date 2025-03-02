from mysol.common.errors import MysolHTTPException

class ArticleNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "게시물을 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)
class NoAuthoriztionError(MysolHTTPException):
    def __init__(self, message: str = "비밀글입니다.") -> None:
        super().__init__(status_code=400, detail=message)
class MissingPassword(MysolHTTPException):
    def __init__(self, message: str = "비밀번호를 입력해야 합니다.") -> None:
        super().__init__(status_code=400, detail=message)
class InvalidPasswordError(MysolHTTPException):
    def __init__(self, message: str = "비밀번호가 일치하지 않습니다.") -> None:
        super().__init__(status_code=400, detail=message)
