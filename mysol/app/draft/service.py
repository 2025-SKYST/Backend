from typing import Annotated

from fastapi import Depends
from mysol.app.draft.dto.responses import DraftListResponse,DraftResponse 
from mysol.app.draft.errors import DraftNotFoundError, NoAuthoriztionError
from mysol.app.blog.errors import BlogNotFoundError
from mysol.app.blog.store import BlogStore
from mysol.app.draft.store import DraftStore
from mysol.app.user.errors import PermissionDeniedError
from mysol.app.user.models import User 

class DraftService:
    def __init__(
        self,
        blog_store: Annotated[BlogStore, Depends()],
        draft_store:Annotated[DraftStore,Depends()]
    ):
        self.blog_store = blog_store
        self.draft_store= draft_store
    
    async def create_draft(
        self, 
        user: User, 
        draft_title: str, 
        draft_content: str, 
    ) -> DraftResponse :
                
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
    
        new_draft = await self.draft_store.create_draft(
            draft_title=draft_title, 
            draft_content=draft_content, 
            blog_id=user_blog.id, 
        )
        
        return DraftResponse.from_draft(new_draft)
    
    async def update_draft(
        self, 
        user: User,
        draft_id: int,
        draft_title: str,
        draft_content: str,
    ) -> DraftResponse:
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        draft = await self.draft_store.get_draft_by_id(draft_id)
        if draft is None: 
            raise DraftNotFoundError()
        # 권한 검증
        if draft.blog_id != user_blog.id:
            raise PermissionDeniedError()
        updated_draft = await self.draft_store.update_draft(
            draft,
            draft_title, 
            draft_content
            )
        return DraftResponse.from_draft(updated_draft)

    async def get_draft_by_id(
        self,
        user,
        draft_id
    )->DraftResponse:

        user_blog=await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()

        draft=await self.draft_store.get_draft_by_id(draft_id)
        if draft is None:
            raise DraftNotFoundError()
        if draft.blog_id !=user_blog.id:
            raise PermissionDeniedError()
        
        return DraftResponse.from_draft(draft)
    
    async def get_drafts_in_blog(
        self,
        user,
        page,
        per_page
    )->DraftListResponse:

        user_blog=await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        return await self.draft_store.get_drafts_in_blog(user_blog.id,page,per_page)
        
    async def delete_draft(
        self,
        user,
        draft_id
    )->None:
        user_blog=await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        draft=await self.draft_store.get_draft_by_id(draft_id)
        if draft.blog_id != user_blog.id:
            raise PermissionDeniedError
        return await self.draft_store.delete_draft(draft)

