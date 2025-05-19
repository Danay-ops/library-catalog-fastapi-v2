from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    genre = Column(String)
    pages = Column(Integer)
    available = Column(Boolean, default=True)
    description = Column(String)
    cover_url = Column(String)




"""id (уникальный идентификатор)
название
автор
год издания
жанр
количество страниц
доступность (в наличии/выдана)
"""