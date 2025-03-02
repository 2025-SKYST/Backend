from mysol.common.errors import MysolHTTPException

class LikeNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "좋아요를 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)
class LikeAlreadyExistsError(MysolHTTPException):
    def __init__(self, message: str = "이미 존재하는 좋아요입니다.") -> None:
        super().__init__(status_code=400, detail=message)