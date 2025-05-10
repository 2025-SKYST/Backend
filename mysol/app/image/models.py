from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysol.database.common import Base, intpk


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    keyword: Mapped[str | None] = mapped_column(Text, nullable=True)
    query: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)

    chapter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chapter.id"), nullable=False
    )
    description_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("description.id"), nullable=True
    )



class Description(Base):
    __tablename__ = "description"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    story: Mapped[str] = mapped_column(Text, nullable=False)
    image_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("image.id"), nullable=False
    )
