from fastapi import APIRouter

from mysol.app.image.views import image_router
from mysol.app.user.views import user_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])