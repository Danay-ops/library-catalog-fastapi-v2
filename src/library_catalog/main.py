from fastapi import FastAPI

from .db.session import engine
from .db.models import Book

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from src.library_catalog.routes.books import router


app = FastAPI()
@app.on_event("startup")
async def on_startup():
    await init_db()

# Регистрируем глобальные обработчики ошибок
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

BOOKS = 'books.json'


# Book.metadata.create_all(bind=engine)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Book.metadata.create_all)

app.include_router(router)


# @app.get("/books", response_model=list[BookSchema])
# async def get_books(author: Optional[str] = None, 
#                     genre: Optional[str] = None, 
#                     skip: int = 0,
#                     limit: int = 100,
#                     service: ServiceBook  = Depends(get_book_service)):
#     """
#     Получить список книг с возможностью фильтрации по автору и жанру.

#     Args:
#         author: Фильтр по автору (опционально)
#         genre: Фильтр по жанру (опционально)


#     Returns:
#         List[BookSchema]: Список книг, соответствующих критериям
#     """

#     return await service.get_all(author, genre, skip, limit)

# @app.get("/books/{title}", response_model=list[BookSchema])
# async def get_book(title: str, service: ServiceBook = Depends(get_book_service)):
#     """
#     Получить книгу по названию.

#     Args:
#         title: Название книги

#     Returns:
#         List[BookSchema]: Список книг, соответствующих критериям
#     """

#     return await service.get_by_title_service(title)

# @app.post("/books", response_model=BookSchema)
# async def add_book( book: BookSchema, 
#                     service: ServiceBook = Depends(get_book_service)):
#     """
#     Добавить новую книгу.

#     Args:
#         book: Книга для добавления

#     Returns:
#         BookSchema: Добавленная книга
#     """

#     return await service.add_new_book(book)

# @app.put("/books", response_model=BookSchema)
# async def update_book(  book: BookSchema, 
#                         service: ServiceBook = Depends(get_book_service)):

#     """
#     Обновить информацию о книге.

#     Args:
#         book: Книга для обновления

#     Returns:
#         BookSchema: Обновленная книга
#     """
    
#     return await service.update(book)

# @app.delete("/books/{book_id}")
# async def delete_book(  book_id: int, 
#                         service: ServiceBook = Depends(get_book_service)):
#     """
#     Удалить книгу по ID.

#     Args:
#         book_id: ID книги для удаления

#     Returns:
#         message: Сообщение об успешном удалении
#     """
#     return await service.delete(book_id)





# @app.get("/books")
# async def get_books():
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
#     return books

# @app.get("/title/{title}")
# async def get_book(title: str):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
#         for book in books:
#             if book['title'] == title:
#                 return book
#         raise  HTTPException(status_code=404, detail="Book not found")
    
# @app.post("/books", response_model=BookSchema)
# async def add_book(book: BookSchema):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
    
#     books.append(book.dict())
    
#     with open (BOOKS, 'w', encoding='utf-8') as f:
#         json.dump(books, f, ensure_ascii=False, indent=4)
#     return book

# @app.put("/books/{title}", response_model=BookSchema)
# async def update_book(title: str, book: BookSchema):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
    
#     for i, b in enumerate(books):
#         if b['title'] == title:
#             books[i] = book.dict()
#             break
#     else:
#         raise  HTTPException(status_code=404, detail="Book not found")
    
#     with open (BOOKS, 'w', encoding='utf-8') as f:
#         json.dump(books, f, ensure_ascii=False, indent=4)
#     return book

# @app.delete("/books/{title}")
# async def delete_book(title: str):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
    
#     for i, b in enumerate(books):
#         if b['title'] == title:
#             books.pop(i)
#             break
#     else:
#         raise  HTTPException(status_code=404, detail="Book not found")
    
#     with open (BOOKS, 'w', encoding='utf-8') as f:
#         json.dump(books, f, ensure_ascii=False, indent=4)
#     return {"message": "Book deleted"}






