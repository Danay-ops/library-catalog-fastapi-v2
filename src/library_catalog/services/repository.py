from typing import Optional
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.library_catalog.services.abstract_book_repository import AbstractBookRepository
from ..db.models import Book
from ..models.schemas import BookSchema
from ..utils.base_api_client import BaseApiClient
from ..core.logger import logger

class SQLBookRepository(AbstractBookRepository):
    def __init__(self, db: Session, cloud: BaseApiClient=None):
        self.db = db
        self.cloud = cloud
    
    async def get(  self,
                    author: Optional[str] = None,
                    genre: Optional[str] = None,
                    skip: int = 0,
                    limit: int = 100
                ):
        
        return await self.get_all(author=author, genre=genre, skip=skip, limit=limit)

    
    async def get_all(  self,
                    author: Optional[str] = None,
                    genre: Optional[str] = None,
                    skip: int = 0,
                    limit: int = 100
                ):
        smth = select(Book)

        if author:
            smth = smth.where(Book.author == author)

        if genre:
            smth = smth.where(Book.genre == genre)

        result = await self.db.execute(smth)

        return result.scalars().all()


    
    async def get_by_title(self, title: str):
        smth = select(Book).where(Book.title == title)
        result = await self.db.execute(smth)
        return result.scalars().all()
    
    async def get_by_id(self, id: int):
        asmth = select(Book).where(Book.id == id)
        result = await self.db.execute(asmth)
        return result.scalars().first()
    
    async def post(self, book: BookSchema):
        return await self.add(book)

    async def add(self, book_data: dict):

        # Проверка на дубликат по ID
        stmt = select(Book).where(Book.id == book_data.get('id'))
        result = await self.db.execute(stmt)
        existing_book = result.scalar_one_or_none()

        if existing_book:
            raise HTTPException(status_code=400, detail='Книга с таким ID уже существует')

        # Создание объекта Book из обогащённого словаря
        db_book = Book(**book_data)
        self.db.add(db_book)
        await self.db.commit()
        await self.db.refresh(db_book)


        return BookSchema.model_validate(db_book)

    
    async def put(self, book: BookSchema):
        return await self.update(book)
    
    async def update(self, book_data: dict):
        logger.info(f'Обновляем книгу {book_data}')
        db_book = await self.get_by_id(book_data.get('id'))

        if db_book is None:
            raise HTTPException(status_code=404, detail=f"Книга с ID {book_data.get('id')} не найдена")


        # Обновляем поля в объекте SQLAlchemy
        for field, value in book_data.items():
            setattr(db_book, field, value)

        await self.db.commit()
        await self.db.refresh(db_book)


        return db_book
    



    async def delete(self, book_id: int):
        logger.info(f'Удаляем книгу с ID {book_id}')
        db_book = await self.get_by_id(book_id)

        if db_book is None:
            raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена")
        
        await self.db.delete(db_book)
        await self.db.commit()


        
        return {'message': f'Книга c ID {book_id} успешно удалена'}

