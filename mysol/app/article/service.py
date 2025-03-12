from typing import Annotated, List, Optional
from fastapi import Depends
from mysol.app.article.dto.responses import (
    ArticleDetailResponse, 
    PaginatedArticleListResponse, 
    ArticleInformationResponse
)
from mysol.app.article.errors import ArticleNotFoundError, NoAuthoriztionError
from mysol.app.article.store import ArticleStore
from mysol.app.blog.errors import BlogNotFoundError
from mysol.app.blog.store import BlogStore
from mysol.app.category.store import CategoryStore
from mysol.app.subscription.store import SubscriptionStore
from mysol.app.notification.service import NotificationService
from mysol.app.user.errors import PermissionDeniedError
from mysol.app.user.models import User 
from mysol.app.image.dto.requests import ImageCreateRequest

class ArticleService:
    def __init__(
        self,
        article_store: Annotated[ArticleStore, Depends()],
        blog_store: Annotated[BlogStore, Depends()],
        category_store: Annotated[CategoryStore, Depends()],
        subscription_store: Annotated[SubscriptionStore, Depends()],
        notification_service: Annotated[NotificationService, Depends()],
    ):
        self.article_store = article_store
        self.blog_store = blog_store
        self.category_store = category_store
        self.subscription_store = subscription_store
        self.notification_service = notification_service

    async def create_article(
        self, 
        user: User, 
        article_title: str, 
        article_content: str, 
        article_description: str,
        main_image_url: Optional[str],
        category_id: int, 
        images: List[ImageCreateRequest],
        problem_numbers : Optional[list[int]] = None,
        secret: int = 0,
        protected: int = 0,
        password: Optional[str] = None,
        comments_enabled: int = 1  # 댓글 기본 허용
    ) -> ArticleDetailResponse:
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        new_article = await self.article_store.create_article(
            article_title=article_title,
            article_content=article_content,
            article_description=article_description,
            main_image_url=main_image_url,
            blog_id=user_blog.id,
            category_id=category_id,
            images=images,
            secret=secret,
            protected=protected,
            password=password,
            comments_enabled=comments_enabled,
            problem_numbers=problem_numbers
        )

        if secret == 0:
            await self.notification_service.add_notification(
                blog_ids=await self.subscription_store.get_subscriber_blog_ids(user_blog.id),
                type=1,
                notification_blog_name=user_blog.blog_name,
                username=user.username,
                notification_blog_image_url=user_blog.main_image_url,
                article_id=new_article.id
            )

        return ArticleDetailResponse.from_article(new_article)
    
    async def update_article(
        self, 
        user: User,
        article_id: int,
        category_id: int,
        images: List[ImageCreateRequest],
        problem_numbers : Optional[list[int]] = None,
        article_title: Optional[str] = None,
        article_content: Optional[str] = None,
        article_description: Optional[str] = None,
        main_image_url: Optional[str] = None,
        secret: Optional[int] = None,
        protected: Optional[int] = None,
        password: Optional[str] = None,
        comments_enabled: Optional[int] = None  # 댓글 허용 여부 수정 가능
    ) -> ArticleDetailResponse:
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        # Article 존재 확인
        article = await self.article_store.get_article_by_id(article_id)
        if article is None: 
            raise ArticleNotFoundError()
        
        # 권한 검증
        if article.blog_id != user_blog.id:
            raise PermissionDeniedError()
        
        
        updated_article = await self.article_store.update_article(
            article=article, 
            category_id=category_id,
            images=images,
            article_title=article_title,
            article_content=article_content,
            article_description=article_description,
            main_image_url=main_image_url,
            secret=secret,
            protected=protected,
            password=password,
            comments_enabled=comments_enabled,
            problem_numbers=problem_numbers
        )

        return ArticleDetailResponse.from_article(updated_article)

    async def get_article_information_by_id(self, user: User, article_id: int, password: Optional[str] = None) -> ArticleInformationResponse:
        article = await self.article_store.get_article_by_id(article_id)
        
        # Article 존재 확인
        if article is None:
            raise ArticleNotFoundError()

        # 비밀글 & 보호된 글 접근 권한 확인
        if article.secret == 1 and article.blog.user_id != user.id:
            raise NoAuthoriztionError()
        if article.blog.user_id != user.id and article.protected == 1 and article.password != password:
            raise NoAuthoriztionError()

        # 조회수 증가
        await self.article_store.increment_article_views(article_id)
        return await self.article_store.get_article_information_by_id(article_id, user, password)

    
    async def get_today_most_viewed(
        self,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_today_most_viewed(user=user)

    async def get_weekly_most_viewed(
        self,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_weekly_most_viewed(user=user)
        
    async def get_articles_in_blog(
        self,
        user: User,
        blog_id: int,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_in_blog(blog_id=blog_id, page=page, per_page=per_page, user=user)
    
    async def get_articles_in_blog_in_category(
        self,
        blog_id: int,
        category_id: int,
        page: int,
        per_page: int,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_in_blog_in_category(
            category_id=category_id, blog_id=blog_id, page=page, per_page=per_page, user=user
        )
    async def get_articles_by_words_and_blog_id(
        self,
        searching_words: str | None,
        blog_id: int | None,
        page: int,
        per_page: int,
        user: User | None,
        sort_by: str = "latest"
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_by_words_and_blog_id(
            searching_words=searching_words,
            blog_id=blog_id,
            page=page,
            per_page=per_page,
            user=user,
            sort_by=sort_by
        )
    
    async def get_articles_of_subscriptions(
        self,
        user : User,
        page: int,
        per_page: int,
    ) -> PaginatedArticleListResponse : 
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        return await self.article_store.get_articles_of_subscriptions(
            user = user, user_blog=user_blog, page = page, per_page = per_page
        )
    
    async def get_top_articles_in_blog(
        self,
        blog_id: int,
        sort_by: str,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_top_articles_in_blog(
            blog_id=blog_id, sort_by=sort_by, user=user)

    async def delete_article(
        self,
        user: User,
        article_id: int,
    ) -> None:

        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)  # await 추가
        if user_blog is None:
            raise BlogNotFoundError()


        # Article 존재 확인
        article = await self.article_store.get_article_by_id(article_id)  # await 추가
        if article is None:
            raise ArticleNotFoundError()

        # 권한 검증
        if article.blog_id != user_blog.id:
            raise PermissionDeniedError()
    

        # Article 삭제
        await self.article_store.delete_article(article)  # await 추가

    async def get_articles_by_problem_number(
        self,
        user: User | None,
        problem_number: int,
        page: int = 1,
        per_page: int = 10,
        sort_by: str = "latest"
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_by_problem_number(
            problem_number=problem_number,
            user=user,
            page=page,
            per_page=per_page,
            sort_by=sort_by
        )
