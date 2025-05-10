from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from memory.database.common import Base, intpk

from memory.app.image.models import Image  
from memory.app.chapter.models import Chapter

class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    login_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    birth: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)  # birth(datetime)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    main_image: Mapped[Optional["Image"]] = relationship(
        "Image",
        back_populates="user",
        uselist=False,
        foreign_keys=[Image.user_id],
    )


class BlockedToken(Base):
    __tablename__ = "blocked_tokens"

    token_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
