from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysol.database.common import Base, intpk

if TYPE_CHECKING:
    from mysol.app.blog.models import Blog
    from mysol.app.comment.models import Comment
    from mysol.app.notification.models import Notification
    from mysol.app.message.models import Message
    from mysol.app.comment.models import Comment


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    blogs: Mapped["Blog"] = relationship(
        "Blog",
        lazy="selectin", 
        back_populates="user", 
        cascade="all, delete-orphan",
        uselist=False
        )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",  # Comment 모델의 article 관계명
        cascade="all, delete-orphan"  # Article 삭제 시 관련된 Comment도 삭제
    )
    notification: Mapped["Notification"] = relationship(
        "Notification", 
        lazy="selectin", 
        back_populates="user", 
        cascade="all, delete-orphan",
        uselist=False
        )

    # 쪽지 송신
    sent_messages: Mapped[list["Message"]] = relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )

    # 쪽지 수신
    received_messages: Mapped[list["Message"]] = relationship(
        "Message",
        foreign_keys="Message.recipient_id",
        back_populates="recipient",
        cascade="all, delete-orphan"
    )

class BlockedToken(Base):
    __tablename__ = "blocked_tokens"

    token_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
