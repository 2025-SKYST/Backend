from pydantic import BaseModel, EmailStr

from mysol.app.user.models import User

class UserSignupResponse(BaseModel):
    email: EmailStr
    username: str

class UserSigninResponse(BaseModel):
    message : str = "로그인 성공"
    username: str

class MyProfileResponse(BaseModel):
    user_id: int
    username: str
    email: str

    @staticmethod
    def from_user(user: User) -> "MyProfileResponse":
        return MyProfileResponse(
            user_id=user.id,
            username=user.username,
            email=user.email,
        )
    
class RefreshResponse(BaseModel):
    message : str = "리프레쉬 성공"