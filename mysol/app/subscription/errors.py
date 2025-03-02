from mysol.common.errors import MysolHTTPException

class SubscriptionAlreadyExistsError(MysolHTTPException):
    def __init__(self, message: str = "이미 존재하는 구독입니다.") -> None:
        super().__init__(status_code=400, detail=message)

class BlogNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "블로그를 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class SubscriptionNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "구독을 찾을 수 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)

class SelfSubscriptionError(MysolHTTPException):
    def __init__(self, message: str = "스스로를 구독할 수는 없습니다.") -> None:
        super().__init__(status_code=404, detail=message)