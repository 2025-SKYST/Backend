from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from mysol.app.message.dto.requests import MessageCreateRequest, MessageUpdateRequest
from mysol.app.message.dto.responses import MessageDetailResponse, PaginatedMessageListResponse
from mysol.app.user.models import User
from mysol.app.message.service import MessageService
from mysol.app.user.views import get_current_user_from_cookie

message_router = APIRouter()

@message_router.post("", status_code=201)
async def send_message(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    message_request: MessageCreateRequest,
    message_service: Annotated[MessageService, Depends()]
) -> MessageDetailResponse:
    return await message_service.create_message(
        sender_id=user.id,
        recipient_id=message_request.recipient_user_id,
        content=message_request.content
    )

@message_router.get("/received", status_code=200)
async def get_received_messages(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    message_service: Annotated[MessageService, Depends()],
    page: int
) -> PaginatedMessageListResponse:
    per_page = 10
    return await message_service.get_received_messages(user_id=user.id, page=page, per_page=per_page)

@message_router.get("/sent", status_code=200)
async def get_sent_messages(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    message_service: Annotated[MessageService, Depends()],
    page: int
) -> PaginatedMessageListResponse:
    per_page = 10
    return await message_service.get_sent_messages(user_id=user.id, page=page, per_page=per_page)

@message_router.get("/{message_id}", status_code=200)
async def read_message(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    message_id: int,
    message_service: Annotated[MessageService, Depends()]
) -> MessageDetailResponse:
    return await message_service.get_message(user_id=user.id, message_id=message_id)

@message_router.delete("/{message_id}", status_code=204)
async def delete_message(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    message_id: int,
    message_service: Annotated[MessageService, Depends()]
) -> None:
    """
    메세지의 내용을 '삭제한 메세지입니다'로 수정
    """
    await message_service.delete_message(user_id=user.id, message_id=message_id)