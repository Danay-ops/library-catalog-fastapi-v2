from abc import ABC, abstractmethod
from typing import Optional, List
from src.library_catalog.models.schemas import BookSchema

class AbstractBookRepository(ABC):

    @abstractmethod
    async def get(self, author: Optional[str], genre: Optional[str], skip: int, limit: int) -> List[BookSchema]:
        pass

    @abstractmethod
    async def get_by_title(self, title: str) -> List[BookSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int):
        pass

    @abstractmethod
    async def add(self, book: BookSchema) -> BookSchema:
        pass

    @abstractmethod
    async def update(self, book: BookSchema):
        pass

    @abstractmethod
    async def delete(self, book_id: int):
        pass
