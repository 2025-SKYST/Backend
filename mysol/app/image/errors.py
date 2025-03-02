from mysol.common.errors import MysolHTTPException

class S3ClientError(MysolHTTPException):
    def __init__(self, message: str = "S3ClientError") -> None:
        super().__init__(status_code=500, detail=message)
class UnexpectedError(MysolHTTPException):
    def __init__(self, message: str = "Unexpected Error") -> None:
        super().__init__(status_code=500, detail=message)
class FileNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "파일을 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)


