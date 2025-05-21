from fastapi import APIRouter, Depends
from typing import Optional

from src.library_catalog.dependencies.dependencies import get_book_service
from src.library_catalog.models.schemas import BookSchema
from src.library_catalog.services.book_service import ServiceBook







router = APIRouter()



@router.get("/books", response_model=list[BookSchema])
async def get_books(author: Optional[str] = None, 
                    genre: Optional[str] = None, 
                    skip: int = 0,
                    limit: int = 100,
                    service: ServiceBook  = Depends(get_book_service)):
    """
    Получить список книг с возможностью фильтрации по автору и жанру.

    Args:
        author: Фильтр по автору (опционально)
        genre: Фильтр по жанру (опционально)


    Returns:
        List[BookSchema]: Список книг, соответствующих критериям
    """

    return await service.get_all(author, genre, skip, limit)

@router.get("/books/{title}", response_model=list[BookSchema])
async def get_book(title: str, service: ServiceBook = Depends(get_book_service)):
    """
    Получить книгу по названию.

    Args:
        title: Название книги

    Returns:
        List[BookSchema]: Список книг, соответствующих критериям
    """

    return await service.get_by_title_service(title)

@router.post("/books", response_model=BookSchema, status_code=201)
async def add_book( book: BookSchema, 
                    service: ServiceBook = Depends(get_book_service)):
    """
    Добавить новую книгу.

    Args:
        book: Книга для добавления

    Returns:
        BookSchema: Добавленная книга
    """

    return await service.add_new_book(book)

@router.put("/books", response_model=BookSchema)
async def update_book(  book: BookSchema, 
                        service: ServiceBook = Depends(get_book_service)):

    """
    Обновить информацию о книге.

    Args:
        book: Книга для обновления

    Returns:
        BookSchema: Обновленная книга
    """
    
    return await service.update(book)

@router.delete("/books/{book_id}")
async def delete_book(  book_id: int, 
                        service: ServiceBook = Depends(get_book_service)):
    """
    Удалить книгу по ID.

    Args:
        book_id: ID книги для удаления

    Returns:
        message: Сообщение об успешном удалении
    """
    return await service.delete(book_id)