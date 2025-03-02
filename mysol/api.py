from fastapi import APIRouter

from mysol.app.article.views import article_router
from mysol.app.blog.views import blog_router
from mysol.app.category.views import category_router
from mysol.app.comment.views import comment_router
from mysol.app.draft.views import draft_router
from mysol.app.image.views import image_router
from mysol.app.like.views import like_router
from mysol.app.message.views import message_router
from mysol.app.notification.views import notification_router
from mysol.app.subscription.views import subscription_router
from mysol.app.user.views import user_router

api_router = APIRouter()

api_router.include_router(article_router, prefix="/articles", tags=["articles"])
api_router.include_router(blog_router, prefix="/blogs", tags=["blogs"])
api_router.include_router(category_router, prefix="/categories", tags=["categories"])
api_router.include_router(comment_router, prefix="/comments", tags=["comments"])
api_router.include_router(draft_router, prefix="/drafts", tags=["drafts"])
api_router.include_router(image_router, prefix="/images", tags=["images"])
api_router.include_router(like_router, prefix="/likes", tags=["likes"])
api_router.include_router(message_router, prefix="/messages", tags=["messages"])
api_router.include_router(notification_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(subscription_router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(user_router, prefix="/users", tags=["users"])

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(blog_router, prefix="/blogs", tags=["blogs"])