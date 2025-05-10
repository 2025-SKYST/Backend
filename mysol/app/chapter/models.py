from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysol.database.common import Base, intpk


# Association table for many-to-many relationship between Chapter and Image
chapter_images = Table(
    "chapter_images",
    Base.metadata,
    Column("chapter_id", ForeignKey("chapter.id"), primary_key=True),
    Column("image_id", ForeignKey("image.id"), primary_key=True),
)

class Chapter(Base):
    __tablename__ = "chapter"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Chapter name with default value
    name: Mapped[str] = mapped_column(Text, server_default="default_name", nullable=False)

    # Content fields
    prologue: Mapped[str | None] = mapped_column(Text, nullable=True)
    epilogue: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Foreign key to a Memoir table
    memoir: Mapped["Memoir"] = relationship("Memoir", back_populates="chapters")

    # Many-to-many relationship to Image
    images: Mapped[list["Image"]] = relationship(
        "Image",
        secondary=chapter_images,
        back_populates="chapters",
        lazy="selectin",
    )

    # Main image (defaults to the first image in .images list upon access)
    main_image_id: Mapped[int | None] = mapped_column(ForeignKey("image.id"), nullable=True)
    main_image: Mapped["Image" | None] = relationship(
        "Image",
        foreign_keys=[main_image_id],
        post_update=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 설정된 이미지를 주입하지 않으면, images 리스트의 첫 번째를 main_image로 설정
        if not self.main_image_id and self.images:
            self.main_image = self.images[0]


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    keyword: Mapped[str | None] = mapped_column(Text, nullable=True)
    query: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"), nullable=False)
    chapter: Mapped[Chapter] = relationship("Chapter", back_populates="images")

    description_id: Mapped[int] = mapped_column(ForeignKey("description.id"), nullable=False)
    description: Mapped["Description"] = relationship("Description", back_populates="images")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

