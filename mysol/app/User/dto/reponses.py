from pydantic import BaseModel, EmailStr

from mysol.app.User.models import User

class UserSignupResponse(BaseModel):
    email: EmailStr
    username: str

class UserSigninResponse(BaseModel):
    message : str = "로그인 성공"
    username: str

class MyProfileResponse(BaseModel):
    username: str
    email: str

    @staticmethod
    def from_user(user: User) -> "MyProfileResponse":
        return MyProfileResponse(
            username=user.username,
            email=user.email,
        )
    
class RefreshResponse(BaseModel):
    message : str = "리프레쉬 성공"