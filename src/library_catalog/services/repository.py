from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..db.models import Book
from ..models.schemas import BookSchema
from ..utils.jsonbin_client import JsonBinClient
from ..utils.library_api import OpenLibraryAPI
from ..utils.base_api_client import BaseApiClient
from ..core.logger import logger

class BookRepository:
    def __init__(self, db: Session, cloud: BaseApiClient=None):
        self.db = db
        self.cloud = cloud
    
    def get(self):
        return self.get_all()

    def get_all(self):
        logger.info('Получаем все книги')
        return self.db.query(Book).all()
    
    def get_by_title(self, title: str):
        return self.db.query(Book).filter(Book.title == title).first()
    
    def get_by_id(self, id: int):
        return self.db.query(Book).filter(Book.id == id).first()
    
    def post(self, book: BookSchema):
        return self.add(book)

    def add(self, book: BookSchema):
        logger.info(f'Добавляем книгу {book}')
        book_data = book.dict()

        # Подчищаем "string", если это заглушка
        if book_data.get("cover_url") == "string":
            book_data["cover_url"] = None
        if book_data.get("description") == "string":
            book_data["description"] = None

        # Обогащение из OpenLibrary
        if not book_data.get('cover_url') or not book_data.get('description'):
            open_library = OpenLibraryAPI()
            extra = open_library.get(title=book.title, author=book.author)
            book_data["cover_url"] = book_data.get("cover_url") or extra.get("cover_url")
            book_data["description"] = book_data.get("description") or extra.get("description")
            
            if not book_data.get('year') and extra.get('first_publish_year'):
                book_data['year'] = extra['first_publish_year']

        # Проверка на дубликат по ID
        if any(b.id == book.id for b in self.get_all()):
            raise HTTPException(status_code=400, detail='Книга с таким ID уже существует')

        # Создание объекта Book из обогащённого словаря
        db_book = Book(**book_data)
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)

        # Добавление в облако — тоже из обработанных данных
        if self.cloud:
            logger.info(f'Добавляем книгу {book.title} в облако')
            self.cloud.post(book_data)

        return BookSchema.from_orm(db_book)
    
    def put(self, book: BookSchema):
        return self.update(book)
    
    def update(self, book: BookSchema):
        logger.info(f'Обновляем книгу {book}')
        db_book = self.get_by_id(book.id)

        if db_book is None:
            raise HTTPException(status_code=404, detail=f"Книга с ID {book.id} не найдена")

        # Получаем словарь из запроса
        book_data = book.dict()

        # Подчищаем "string", если это заглушка
        if book_data.get("cover_url") == "string":
            book_data["cover_url"] = None
        if book_data.get("description") == "string":
            book_data["description"] = None

        # Обогащение из OpenLibrary
        open_library = OpenLibraryAPI()
        extra = open_library.get(title=book.title, author=book.author)

        if not book_data.get('cover_url') and extra.get('cover_url'):
            book_data['cover_url'] = extra['cover_url']

        if not book_data.get('description') and extra.get('description'):
            book_data['description'] = extra['description']

        if not book_data.get('year') and extra.get('first_publish_year'):
            book_data['year'] = extra['first_publish_year']

        # Обновляем поля в объекте SQLAlchemy
        for field, value in book_data.items():
            setattr(db_book, field, value)

        self.db.commit()
        self.db.refresh(db_book)



        # Отправляем в облако обновлённые данные
        if self.cloud:
            logger.info(f'Обновляем книгу {book.title} в облаке')
            self.cloud.put(book_data)

        return db_book


    def delete(self, book_id: int):
        logger.info(f'Удаляем книгу с ID {book_id}')
        db_book = self.get_by_id(book_id)

        if db_book is None:
            raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена")
        
        self.db.delete(db_book)
        self.db.commit()

        # Добавление в облако — тоже из обработанных данных
        if self.cloud:
            logger.info(f'Удаляем книгу с ID {book_id} из облака')
            self.cloud.delete(book_id)
        
        return {'message': f'Книга c ID {book_id} успешно удалена'}