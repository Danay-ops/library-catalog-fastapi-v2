from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.utils.library_api import OpenLibraryAPI
from src.library_catalog.services.cloud_repositiry import CloudBookRepository
from src.library_catalog.services.abstract_book_repository import AbstractBookRepository
from src.library_catalog.db.session import get_db
from src.library_catalog.services.book_service import ServiceBook
from src.library_catalog.services.repository import SQLBookRepository
from src.library_catalog.utils.jsonbin_client import JsonBinClient


def get_json_bin_client() -> JsonBinClient:
    return JsonBinClient()

def get_book_repo(  db: AsyncSession=Depends(get_db), 
                    cloud_client: JsonBinClient=Depends(get_json_bin_client)) -> AbstractBookRepository:
    return SQLBookRepository(db,cloud_client)

def get_cloud_repo(  cloud_client: JsonBinClient=Depends(get_json_bin_client)) -> AbstractBookRepository:
    return CloudBookRepository(cloud_client)

def get_open_library_api() -> OpenLibraryAPI:
    return OpenLibraryAPI()

def get_book_service(
    repo: AbstractBookRepository = Depends(get_book_repo),
    cloud_repo: AbstractBookRepository = Depends(get_cloud_repo),
    open_library: OpenLibraryAPI = Depends(get_open_library_api)) -> ServiceBook:
    return ServiceBook(sql_repo=repo, cloud_repo=cloud_repo, open_library=open_library)