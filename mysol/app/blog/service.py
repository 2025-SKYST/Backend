from typing import Annotated

from fastapi import Depends
from mysol.app.blog.models import Blog
from mysol.app.user.models import User
from mysol.app.blog.store import BlogStore
from mysol.app.blog.dto.responses import BlogDetailResponse, PaginatedBlogDetailResponse
from mysol.app.blog.errors import BlogNotFoundError
from mysol.app.category.store import CategoryStore
from mysol.app.user.store import UserStore


class BlogService:
    def __init__(self, blog_store: Annotated[BlogStore, Depends()], category_store: Annotated[CategoryStore, Depends()], user_store: Annotated[UserStore, Depends()]) -> None:
        self.blog_store = blog_store
        self.categroy_store = category_store
        self.user_store = user_store

    async def create_blog(
        self,
        user_id : str,
        blog_name : str,
        description: str
    ) -> BlogDetailResponse:

        blog = await self.blog_store.add_blog(user_id=user_id, blog_name=blog_name, description=description)

        default_category=await self.categroy_store.create_category(blog_id=blog.id, categoryname="카테고리 없음", categorylevel=1)
        await self.blog_store.update_blog(user_id=user_id, new_default_category_id=default_category.id, new_blog_name=None, description=None, new_main_image_URL=None)

        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def get_blog_by_id(self, blog_id : int) -> BlogDetailResponse:
        blog=await self.blog_store.get_blog_by_id(blog_id)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)

    async def get_blog_by_user(self, user : User) -> BlogDetailResponse:
        blog = await self.blog_store.get_blog_of_user(user.id)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def get_blog_by_userid(self, user_id : int) -> BlogDetailResponse:
        blog = await self.blog_store.get_blog_of_user(user_id)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)

    async def update_blog(
        self,
        user_id: int,
        new_blog_name : str | None,
        new_description : str |None,
        new_default_category_id : int|None,
        new_main_image_URL : str | None
    ) -> BlogDetailResponse:
        updated_blog = await self.blog_store.update_blog(
            user_id=user_id,
            new_blog_name=new_blog_name,
            description=new_description,
            new_default_category_id=new_default_category_id,
            new_main_image_URL=new_main_image_URL
        )
        return BlogDetailResponse.model_validate(updated_blog, from_attributes=True)
    
    async def get_blog_by_user_email(self, email: str) -> BlogDetailResponse:
        """
        이메일을 통해 유저의 블로그 조회
        """
        # 이메일로 유저 정보 조회
        user = await self.user_store.get_user_by_email(email)
        if not user:
            raise BlogNotFoundError

        # 유저의 블로그 조회
        blog = await self.blog_store.get_blog_of_user(user_id=user.id)
        if not blog:
            raise BlogNotFoundError

        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def search_blog_by_keywords(self, keywords: str, page: int, per_page: int) -> PaginatedBlogDetailResponse:
        """
        키워드로 블로그 검색
        """
        # 검색된 블로그와 총 개수를 반환
        blogs = await self.blog_store.search_blogs_by_keywords(keywords, page, per_page)
        total_count = await self.blog_store.count_search_result_by_keywords(keywords)

        # 블로그 목록을 DTO로 변환
        blog_responses = [
            BlogDetailResponse.model_validate(blog, from_attributes=True) for blog in blogs
        ]

        # 페이지네이션 응답 생성
        return PaginatedBlogDetailResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            blogs=blog_responses,
        )