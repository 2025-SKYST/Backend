from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from mysol.app.article.dto.requests import ArticleCreateRequest, ArticleUpdateRequest
from mysol.app.article.dto.responses import PaginatedArticleListResponse, ArticleDetailResponse, ArticleInformationResponse
from mysol.app.article.service import ArticleService
from mysol.app.blog.service import BlogService

from mysol.app.user.models import User
from mysol.app.image.models import Image
from mysol.app.user.views import get_current_user_from_cookie


article_router = APIRouter()

# article 생성
@article_router.post("/create", status_code=201)
async def create_article(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    article: ArticleCreateRequest,
    article_service: Annotated[ArticleService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
) -> ArticleDetailResponse:
    user_blog = await blog_service.get_blog_by_user(user)



    if article.category_id == 0:
        return await article_service.create_article(
            user=user, 
            article_title=article.title, 
            article_content=article.content, 
            article_description= article.description, 
            main_image_url = article.main_image_url,
            category_id=user_blog.default_category_id,
            secret=article.secret,
            images = article.images,
            protected=article.protected,
            password=article.password,
            comments_enabled=article.comments_enabled,
            problem_numbers=article.problem_numbers
            )
    else:
        return await article_service.create_article(
            user=user, 
            article_title=article.title, 
            article_content=article.content, 
            article_description = article.description,
            main_image_url = article.main_image_url, 
            category_id=article.category_id,
            secret=article.secret,
            images = article.images,
            protected=article.protected,
            password=article.password,
            comments_enabled=article.comments_enabled,
            problem_numbers=article.problem_numbers
            )

# article 수정
@article_router.patch("/update/{article_id}", status_code=200)
async def update_article(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    article_id: int,
    article: ArticleUpdateRequest,
    article_service: Annotated[ArticleService, Depends()],
    blog_service: Annotated[BlogService, Depends()],

) -> ArticleDetailResponse:
    user_blog = await blog_service.get_blog_by_user(user)
    if article.category_id == 0:
        return await article_service.update_article(
            user=user,
            article_id = article_id,
            article_title=article.title, 
            article_content=article.content, 
            article_description = article.description, 
            main_image_url = article.main_image_url,
            category_id=user_blog.default_category_id,
            images = article.images,
            secret = article.secret,
            protected=article.protected,
            password=article.password,
            comments_enabled=article.comments_enabled,
            problem_numbers=article.problem_numbers
        )
    else : 
        return await article_service.update_article(
            user=user, 
            article_id = article_id,
            article_title=article.title, 
            article_content=article.content, 
            article_description = article.description, 
            main_image_url = article.main_image_url,
            category_id = article.category_id,
            images = article.images,
            secret = article.secret,
            protected=article.protected,
            password=article.password,
            comments_enabled=article.comments_enabled,
            problem_numbers=article.problem_numbers
        )


# article 정보 가져오기
@article_router.get("/get/{article_id}", status_code=200)
async def get_article_information_by_id(
    article_service: Annotated[ArticleService, Depends()],
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    article_id : int,
    password: Optional[str] = Query(None, description="보호된 글의 비밀번호")
) -> ArticleInformationResponse :
    return await article_service.get_article_information_by_id(user, article_id, password)

# blog 내 인기글 가져오기
@article_router.get("/today_mysol", status_code=200)
async def get_today_most_viewed(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
) ->PaginatedArticleListResponse:
    return await article_service.get_today_most_viewed(
        user = user
    )
# blog 내 인기글 가져오기
@article_router.get("/weekly_mysol", status_code=200)
async def get_weekly_most_viewed(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
) ->PaginatedArticleListResponse:
    return await article_service.get_weekly_most_viewed(
        user = user
    )

# blog 내 인기글 가져오기
@article_router.get("/blogs/{blog_id}/sort_by/{sort_by}", status_code=200)
async def get_top_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
    blog_id : int,
    sort_by: str
) ->PaginatedArticleListResponse:
    return await article_service.get_top_articles_in_blog(
        blog_id = blog_id,
        sort_by = sort_by,
        user = user
    )

# blog 내 article 목록 가져오기
@article_router.get("/blogs/{blog_id}", status_code=200)
async def get_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
    blog_id : int,
    page: int
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_in_blog(
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )

# blog 내 특정 category 내 article 목록 가져오기
@article_router.get("/blogs/{blog_id}/categories/{category_id}", status_code=200)
async def get_articles_in_blog_in_category(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
    category_id : int,
    blog_id: int,
    page: int
) ->PaginatedArticleListResponse:
    per_page = 10

    return await article_service.get_articles_in_blog_in_category(
        category_id = category_id, 
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )
# blog 내 subscription 목록에서 article 가져오기
@article_router.get("/blogs/{blog_id}/subscription", status_code=200)
async def get_articles_of_subscription(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    article_service: Annotated[ArticleService, Depends()],
    page: int
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_of_subscriptions(
        user = user,
        page = page,
        per_page = per_page
    )

# blog 내 인기글 가져오기
@article_router.get("/blogs/{blog_id}/sort_by/{sort_by}", status_code=200)
async def get_top_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
    blog_id : int,
    sort_by: str
) ->PaginatedArticleListResponse:
    return await article_service.get_top_articles_in_blog(
        blog_id = blog_id,
        sort_by = sort_by,
        user=user
    )


# 특정 blog 내에서의 검색 기능 지원
@article_router.get("/search/{blog_id}/{searching_words}", status_code=200)
async def get_articles_by_words_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
    page: int,
    searching_words: str | None = None,
    blog_id : int | None = None
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_by_words_and_blog_id(
        searching_words = searching_words, 
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )

# 전체 검색 기능 지원
@article_router.get("/search/{searching_words}", status_code=200)
async def get_articles_by_word(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(get_current_user_from_cookie)],
    page: int,
    searching_words: str,
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_by_words_and_blog_id(
        searching_words = searching_words, 
        blog_id = None,
        page = page,
        per_page = per_page,
        user=user
    )

# article 삭제
@article_router.delete("/delete/{article_id}", status_code=204)
async def delete_article(
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    article_id: int,
    article_service: Annotated[ArticleService, Depends()],
) -> None:
    await article_service.delete_article(user, article_id)

# 특정 문제 번호를 포함하는 게시글 가져오기
@article_router.get("/problems/{problem_number}", status_code=200)
async def get_articles_by_problem_number(
    article_service: Annotated[ArticleService, Depends()],
    user: Annotated[User, Depends(get_current_user_from_cookie)],
    problem_number: int,
    page: int = Query(1, alias="page"),
    per_page: int = Query(10, alias="per_page")
) -> PaginatedArticleListResponse:
    return await article_service.get_articles_by_problem_number(
        user=user,
        problem_number=problem_number,
        page=page,
        per_page=per_page
    )
