from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, Text, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from memory.database.common import Base, intpk

if TYPE_CHECKING:
    from memory.app.chapter.models import Chapter
    from memory.app.user.models import User

class Image(Base):
    __tablename__ = "image"

    id: Mapped[intpk]
    file_url: Mapped[str] = mapped_column(String(600), nullable=False)
    chapter_id: Mapped[int | None] = mapped_column(ForeignKey("chapter.id", ondelete="CASCADE"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    is_main: Mapped[bool] = mapped_column(default=False)

    content : Mapped[str | None] = mapped_column(Text, nullable = True)

    chapter: Mapped["Chapter"] = relationship(
        "Chapter",
        back_populates="images",
        foreign_keys=[chapter_id],
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="main_image",
        foreign_keys=[user_id],
    )