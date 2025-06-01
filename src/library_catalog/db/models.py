from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

class Base(DeclarativeBase):
    pass



class Book(Base):
    """id (уникальный идентификатор)
    название
    автор
    год издания
    жанр
    количество страниц
    доступность (в наличии/выдана)
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    genre: Mapped[str] = mapped_column()
    pages: Mapped[int] = mapped_column()
    available: Mapped[bool] = mapped_column(default=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    cover_url: Mapped[Optional[str]] = mapped_column(nullable=True)




