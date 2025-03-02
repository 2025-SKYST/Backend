from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysol.database.common import Base, intpk

if TYPE_CHECKING:
    from mysol.app.user.models import User
    from mysol.app.category.models import Category
    from mysol.app.article.models import Article
    from mysol.app.comment.models import Comment
    from mysol.app.subscription.models import Subscription
    from mysol.app.like.models import Like
    from mysol.app.notification.models import Notification
    from mysol.app.draft.models import Draft
    from mysol.app.image.models import Image

class Blog(Base):
    __tablename__ = "blog"
    __table_args__ = (
        UniqueConstraint("user_id", name="unique_user_blog"),
    )

    id: Mapped[intpk] # 블로그 아이디
    blog_name: Mapped[str] = mapped_column(String(100), nullable=False)  # 블로그 제목
    description: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)

    main_image_url: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)
    main_image : Mapped["Image"] = relationship("Image", back_populates = "blog")

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())  # 생성 시간
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())  # 갱신 시간
    default_category_id: Mapped[int|None] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  # 블로그 소유자
    
    # 관계 설정
    user: Mapped["User"] = relationship("User", back_populates="blogs")
    categories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="blog", cascade="all, delete-orphan"
        )

    articles: Mapped[list["Article"]] = relationship(
        "Article",  back_populates="blog", cascade="all, delete-orphan"
        )

    drafts: Mapped[list["Draft"]]=relationship(
        "Draft", back_populates="blog", cascade="all, delete-orphan"
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", foreign_keys="Subscription.subscriber_id", back_populates="subscriber"
    )  # 이 블로그가 구독한 다른 블로그들

    subscribers: Mapped[list["Subscription"]] = relationship(
        "Subscription", foreign_keys="Subscription.subscribed_id", back_populates="subscribed_blog"
    )  # 이 블로그를 구독한 다른 블로그들

    likes: Mapped[list["Like"]] = relationship("Like", back_populates ="blog", cascade = "all,delete-orphan")
    # 이 블로그가 누른 like 의 모음

    notification: Mapped[list["Notification"]] = relationship("Notification", back_populates ="blog", cascade = "all,delete-orphan")

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="blog", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Blog id={self.id}, blog_name={self.blog_name}, user_id={self.user_id}>"