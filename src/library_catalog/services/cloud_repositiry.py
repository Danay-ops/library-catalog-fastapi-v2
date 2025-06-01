from src.library_catalog.utils.base_api_client import BaseApiClient
from src.library_catalog.services.abstract_cloud_repository import AbstractCloudRepository
from src.library_catalog.core.logger import logger

class CloudBookRepository(AbstractCloudRepository):
    def __init__(self, cloud: BaseApiClient = None):
        self.cloud = cloud
    
    async def add(self, book_data: dict):
        if self.cloud:
            logger.info(f'Добавляем книгу(CloudBookRepository) {book_data.get("title")} в облако')
            self.cloud.post(book_data)
    
    async def update(self, book_data: dict):
        if self.cloud:
            logger.info(f'Обновляем книгу(CloudBookRepository) {book_data.get("title")} в облаке')
            self.cloud.put(book_data)
    
    async def delete(self, book_id: int):
        if self.cloud:
            logger.info(f'Удаляем книгу(CloudBookRepository) {book_id} из облака')
            self.cloud.delete(book_id)