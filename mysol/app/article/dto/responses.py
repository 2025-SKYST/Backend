from fastapi import Depends
from typing import Annotated, Optional
from typing_extensions import Self
from pydantic import BaseModel
from datetime import datetime
from mysol.app.article.models import Article
from mysol.app.article.errors import ArticleNotFoundError
from mysol.app.blog.store import BlogStore
from mysol.app.user.models import User


class ArticleInformationResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    article_main_image_url: Optional[str] = None
    protected: int
    comments_enabled: int

    blog_id: int
    blog_name: str
    blog_main_image_url: Optional[str] = None
    category_id: int

    secret: int
    views: int

    password: Optional[str] = None

    article_likes: int
    article_comments: int

    problem_numbers: list[int] = []

    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(
        article: Optional[Article], 
        blog_name: str, 
        blog_main_image_url: Optional[str], 
        article_likes: int, 
        article_comments: int
    ) -> Self:
        if article is None:
            raise ArticleNotFoundError

        return ArticleInformationResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            created_at=article.created_at,
            updated_at=article.updated_at,
            article_main_image_url=article.main_image_url,
            views=article.views,
            blog_id=article.blog_id,
            category_id=article.category_id,
            blog_name=blog_name,
            blog_main_image_url=blog_main_image_url,
            article_likes=article_likes,
            article_comments=article_comments,
            protected=article.protected,
            comments_enabled=article.comments_enabled,
            secret=article.secret,
            password=article.password,
            problem_numbers=article.problem_numbers or []
        )


class ArticleDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    views: int
    protected: int
    comments_enabled: int
    secret: int
    problem_numbers: list[int] = []

    @staticmethod
    def from_article(article: Article) -> Self:
        return ArticleDetailResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            created_at=article.created_at,
            updated_at=article.updated_at,
            views=article.views,
            protected=article.protected,
            comments_enabled=article.comments_enabled,
            secret=article.secret,
            problem_numbers=article.problem_numbers or []
        )


class ArticleSearchInListResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    article_main_image_url: Optional[str] = None

    blog_id: int
    blog_name: str
    blog_main_image_url: Optional[str] = None

    views: int
    article_likes: int
    article_comments: int
    protected: int
    secret: int

    problem_numbers: list[int] = []

    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(
        article: Optional[Article], 
        blog_name: str, 
        blog_main_image_url: Optional[str], 
        article_likes: int, 
        article_comments: int,
        user: User 
    ) -> Self:
        if article is None:
            raise ArticleNotFoundError
        
        # 🔥 description 80자 제한 로직 추가
        if article.protected == 0 or article.blog.user_id == user.id:
            return_description = article.description[:80] + "…" if len(article.description) > 80 else article.description
        else:
            return_description = "🔒 보호된 게시글입니다."

        return ArticleSearchInListResponse(
            id=article.id,
            title=article.title,
            description=return_description,
            created_at=article.created_at,
            updated_at=article.updated_at,
            article_main_image_url=article.main_image_url,
            views=article.views,
            blog_id=article.blog_id,
            blog_name=blog_name,
            blog_main_image_url=blog_main_image_url,
            article_likes=article_likes,
            article_comments=article_comments,
            protected=article.protected,
            secret=article.secret,
            problem_numbers=article.problem_numbers or []
        )


class PaginatedArticleListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    articles: list[ArticleSearchInListResponse]
