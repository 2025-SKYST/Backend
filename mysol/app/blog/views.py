from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from mysol.app.blog.dto.requests import BlogCreateRequest, BlogUpdateRequest
from mysol.app.blog.dto.responses import BlogDetailResponse, PaginatedBlogDetailResponse
from mysol.app.user.models import User
from mysol.app.blog.service import BlogService
from mysol.app.user.views import get_current_user_from_cookie

blog_router = APIRouter()


@blog_router.post("", status_code=HTTP_201_CREATED)
async def create_blog(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    blog_service: Annotated[BlogService, Depends()],
    blog_create_request: BlogCreateRequest
) -> BlogDetailResponse:
    return await blog_service.create_blog(
        user_id=user.id,
        blog_name=blog_create_request.blog_name,
        description=blog_create_request.description
    )

@blog_router.get("/search", response_model=PaginatedBlogDetailResponse, status_code=HTTP_200_OK)
async def search_blogs(
    keywords: str,
    page: int,
    blog_service: Annotated[BlogService, Depends()]
) -> PaginatedBlogDetailResponse:
    """
    키워드로 블로그 검색 API
    """
    per_page=10
    return await blog_service.search_blog_by_keywords(keywords=keywords, page=page, per_page=per_page)

@blog_router.get("/my_blog")
async def get_blog_by_user(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    blog_service: Annotated[BlogService, Depends()]
) -> BlogDetailResponse:
    if user:
        print("user found")
    else:
        print("user not found")
    return await blog_service.get_blog_by_user(user)

@blog_router.get("/by_id/{blog_id}", response_model=BlogDetailResponse, status_code=HTTP_200_OK)
async def get_blog_by_id(
    blog_id: int,
    blog_service: Annotated[BlogService, Depends()]
) -> BlogDetailResponse:
    """
    블로그 아이디로 블로그 조회 API
    """
    return await blog_service.get_blog_by_id(blog_id)

@blog_router.get("/by_userid/{user_id}", response_model=BlogDetailResponse, status_code=HTTP_200_OK)
async def get_blog_by_id(
    user_id: int,
    blog_service: Annotated[BlogService, Depends()]
) -> BlogDetailResponse:
    """
    유저 아이디로 블로그 조회 API
    """
    return await blog_service.get_blog_by_userid(user_id)

@blog_router.get("/by_email/{email}", response_model=BlogDetailResponse, status_code=HTTP_200_OK)
async def get_blog_by_email(
    email: str,
    blog_service: Annotated[BlogService, Depends()]
) -> BlogDetailResponse:
    """
    유저 이메일로 블로그 조회 API
    """
    return await blog_service.get_blog_by_user_email(email)