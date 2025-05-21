

from typing import Optional

from fastapi import HTTPException
from src.library_catalog.services.abstract_cloud_repository import AbstractCloudRepository
from src.library_catalog.utils.library_api import OpenLibraryAPI
from src.library_catalog.models.schemas import BookSchema
from src.library_catalog.services.repository import AbstractBookRepository
from src.library_catalog.core.logger import logger


class ServiceBook:
    def __init__(   self, sql_repo: AbstractBookRepository = None, cloud_repo: AbstractCloudRepository = None, 
                    open_library: OpenLibraryAPI = None):
        self.sql_repo = sql_repo
        self.cloud_repo = cloud_repo
        self.open_library = open_library
    
    async def get_all(self, author: Optional[str] = None, genre: Optional[str] = None, skip: int = 0, limit: int = 100):
        books = await self.sql_repo.get_all()

        return await self.sql_repo.get_all(author=author, genre=genre, skip=skip, limit=limit)
    
    async def get_by_title_service(self, title: str):
        book = await self.sql_repo.get_by_title(title)
        if not book:
            raise HTTPException(status_code=404, detail=f"Книга с названием '{title}' не найдена")
        return book
    
    async def add_new_book(self, book: BookSchema):
        logger.info(f'Добавляем книгу {book}')
        book_data = book.dict()

        # Подчищаем "string", если это заглушка
        if book_data.get("cover_url") == "string":
            book_data["cover_url"] = None
        if book_data.get("description") == "string":
            book_data["description"] = None

        # Обогащение из OpenLibrary
        if not book_data.get('cover_url') or not book_data.get('description'):
            open_library = self.open_library
            extra = open_library.get(title=book.title, author=book.author)
            book_data["cover_url"] = book_data.get("cover_url") or extra.get("cover_url")
            book_data["description"] = book_data.get("description") or extra.get("description")
            
            if not book_data.get('year') and extra.get('first_publish_year'):
                book_data['year'] = extra['first_publish_year']
        
        # Добавляем в базу
        created_book = await self.sql_repo.add(book_data)

        # Добавляем в облако
        await self.cloud_repo.add(book_data)

        return created_book
    
    async def update(self, book: BookSchema):
        logger.info(f'Обновляем книгу {book}')
        

        # Получаем словарь из запроса
        book_data = book.dict()

        # Подчищаем "string", если это заглушка
        if book_data.get("cover_url") == "string":
            book_data["cover_url"] = None
        if book_data.get("description") == "string":
            book_data["description"] = None

        # Обогащение из OpenLibrary
        open_library = self.open_library
        extra = open_library.get(title=book.title, author=book.author)

        if not book_data.get('cover_url') and extra.get('cover_url'):
            book_data['cover_url'] = extra['cover_url']

        if not book_data.get('description') and extra.get('description'):
            book_data['description'] = extra['description']

        if not book_data.get('year') and extra.get('first_publish_year'):
            book_data['year'] = extra['first_publish_year']
        
        updated_book = await self.sql_repo.update(book_data)

        # Обновляем в облаке
        await self.cloud_repo.update(book_data)

        return updated_book
    
    async def delete(self, book_id: int):
        logger.info(f"Удаляем книгу(ServiceBook) {book_id}")
        await self.cloud_repo.delete(book_id)

        return await self.sql_repo.delete(book_id)
