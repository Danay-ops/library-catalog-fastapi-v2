



from abc import ABC, abstractmethod


class AbstractCloudRepository(ABC):

    @abstractmethod
    async def add(self, book_data: dict):
        pass

    @abstractmethod
    async def update(self, book_data: dict):
        pass

    @abstractmethod 
    async def delete(self, book_data: dict):
        pass
