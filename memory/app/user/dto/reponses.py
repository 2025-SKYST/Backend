from pydantic import BaseModel, EmailStr

from mysol.app.user.models import User

class UserSignupResponse(BaseModel):
    username: str

class UserSigninResponse(BaseModel):
    access_token : str
    refresh_token : str

from pydantic import BaseModel
from datetime import datetime

class MyProfileResponse(BaseModel):
    user_id: int
    username: str
    login_id: str
    birth: datetime | None  # nullable 허용

    @staticmethod
    def from_user(user: User) -> "MyProfileResponse":
        return MyProfileResponse(
            user_id=user.id,
            username=user.username,
            login_id=user.login_id,
            birth=user.birth,
        )
    
class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str