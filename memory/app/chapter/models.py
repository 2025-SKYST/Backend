from typing import TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, Text, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from memory.database.common import Base, intpk

if TYPE_CHECKING:
    from memory.app.user.models import User
    from memory.app.image.models import Image

class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[intpk]
    chapter_name: Mapped[str] = mapped_column(String(100), nullable=False)

    prologue: Mapped[str | None] = mapped_column(Text, nullable=True)
    epilogue: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="chapters",
    )

    images: Mapped[List["Image"]] = relationship(
        "Image",
        back_populates="chapter",
        cascade="all, delete-orphan",
        lazy="selectin",
    )