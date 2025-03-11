from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from mysol.app.notification.dto.requests import NotificationDeleteRequest, NotificationCheckRequest
from mysol.app.notification.dto.responses import NotificationResponse, NotificationListResponse, PaginatedNotificationListResponse
from mysol.app.user.models import User
from mysol.app.notification.models import Notification
from mysol.app.notification.service import NotificationService
from mysol.app.user.views import get_current_user_from_header

notification_router = APIRouter()


# @notification_router.get("/my_notifications")
# async def get_notifications_by_user(
#     user: Annotated[User, Depends(get_current_user_from_header)],
#     notification_service: Annotated[NotificationService, Depends()]
# ):
#     notifications: list[Notification] = await notification_service.get_notifications_by_user(user)
#     response = NotificationListResponse(
#         total_count=len(notifications),
#         notifications=[NotificationResponse.from_notification(n) for n in notifications]
#     )
#     return response
@notification_router.get("/my_notifications")
async def get_notifications_by_user(
    user: Annotated[User, Depends(get_current_user_from_header)],
    notification_service: Annotated[NotificationService, Depends()],
    page: int,
    type: Optional[int] = None,
) -> PaginatedNotificationListResponse:
    per_page = 10
    return await notification_service.get_notifications_by_user(
        user=user,
        page=page,
        per_page=per_page,
        type=type
        )

@notification_router.delete("/my_notifications")
async def delete_notification(
    user: Annotated[User, Depends(get_current_user_from_header)],
    notification_delete_request: NotificationDeleteRequest,
    notification_service: Annotated[NotificationService, Depends()]
)->str:
    await notification_service.delete_notification_by_id(user=user, notification_id=notification_delete_request.notification_id)
    return "Success"

@notification_router.patch("/my_notifications")
async def check_notification(
    user: Annotated[User, Depends(get_current_user_from_header)],
    notification_check_request: NotificationCheckRequest,
    notification_service: Annotated[NotificationService, Depends()]
) -> str:
    await notification_service.check_notification(user=user, notification_id=notification_check_request.notification_id)
    return "Success"