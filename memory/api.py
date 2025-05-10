from fastapi import APIRouter

from memory.app.user.views import user_router
from memory.app.chapter.views import chapter_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(chapter_router, prefix="/chapters", tags=["chapters"])