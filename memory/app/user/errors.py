from memory.common.errors import MysolHTTPException

class LoginIdAlreadyExistsError(MysolHTTPException):
    def __init__(self, message: str = "이미 존재하는 이메일입니다.") -> None:
        super().__init__(status_code=409, detail=message)

class UserNameAlreadyExistsError(MysolHTTPException):
    def __init__(self, message: str = "이미 존재하는 유저이름입니다.") -> None:
        super().__init__(status_code=409, detail=message)

class UserUnsignedError(MysolHTTPException):
    def __init__(self, message: str = "존재하지 않는 유저입니다.") -> None:
        super().__init__(status_code=404, detail=message)

class InvalidPasswordError(MysolHTTPException):
    def __init__(self, message: str = "비밀번호가 일치하지 않습니다.") -> None:
        super().__init__(status_code=400, detail=message)

class UserNotFoundError(MysolHTTPException):
    def __init__(self, message: str = "존재하지 않는 유저입니다.") -> None:
        super().__init__(status_code=404, detail=message)

class ExpiredSignatureError(MysolHTTPException):
    def __init__(self, message: str="토큰이 만료되었습니다.") -> None:
        super().__init__(status_code=401, detail=message)
class InvalidTokenError(MysolHTTPException):
    def __init__(self, message: str="올바르지 않은 토큰입니다."):
        super().__init__(status_code=401, detail=message)
class BlockedTokenError(MysolHTTPException):
    def __init__(self, message: str="차단된 토큰입니다.") -> None:
        super().__init__(status_code=401, detail=message)
class MissingAccessTokenError(MysolHTTPException):
    def __init__(self, message: str="로그인 된 상태가 아닙니다.") -> None:
        super().__init__(status_code=401, detail=message)
class PermissionDeniedError(MysolHTTPException):
    def __init__(self, message: str="접근이 거부되었습니다.") -> None:
        super().__init__(status_code=401, detail=message)