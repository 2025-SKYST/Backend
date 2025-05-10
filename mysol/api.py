from fastapi import APIRouter

from mysol.app.user.views import user_router
#from mysol.app.chapter.views import chapter_router
from mysol.app.image.views import image_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
#api_router.include_router(chapter_router, prefix="/chapters", tags=["chapters"])
api_router.include_router(image_router, prefix="/images", tags=["images"])

