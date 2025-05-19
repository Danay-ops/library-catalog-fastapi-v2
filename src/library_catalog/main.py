from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi import Depends
from .db.session import get_db, engine
from .services.repository import BookRepository
from sqlalchemy.orm import Session
from .utils.jsonbin_client import JsonBinClient
from .db.models import Book
from .models.schemas import BookSchema
import json
import os

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)




app = FastAPI()


# Регистрируем глобальные обработчики ошибок
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

BOOKS = 'books.json'


Book.metadata.create_all(bind=engine)

cloud_client = JsonBinClient()


@app.get("/books")
async def get_books(author: Optional[str] = None, 
                    genre: Optional[str] = None, 
                    db: Session = Depends(get_db)):
    
    repo = BookRepository(db)

    all_books = repo.get_all()

    if author:
        all_books = [b for b in all_books if author in b.author]

    if genre:
        all_books = [b for b in all_books if genre in b.genre]
    
    return all_books

@app.get("/title/{title}")
async def get_book(title: str, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.get_by_title(title)
    if not book:
        raise HTTPException(status_code=404, detail=f"Книга с названием '{title}' не найдена")
    return book

@app.post("/books", response_model=BookSchema)
async def add_book(book: BookSchema, db: Session = Depends(get_db)):
    repo = BookRepository(db, cloud_client)

    return repo.add(book)

@app.put("/books", response_model=BookSchema)
async def update_book(book: BookSchema, db: Session = Depends(get_db)):
    repo = BookRepository(db, cloud_client)

    return repo.update(book)

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db, cloud_client)

    return repo.delete(book_id)





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






