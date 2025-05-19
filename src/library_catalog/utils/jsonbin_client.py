import os
import json
from fastapi import HTTPException
import requests
from ..core.setings import API_KEYS, BIN_ID
from .library_api import OpenLibraryAPI
from .base_api_client import BaseApiClient
from ..core.logger import logger

class JsonBinClient(BaseApiClient):
    def __init__(self):
        self.api_key = API_KEYS
        self.base_url = 'https://api.jsonbin.io/v3/b/'
        self.bin_id = BIN_ID
    
    # def get_books(self) -> dict:
    #     url = f'{self.base_url}{self.bin_id}'
    #     headers = {'X-Access-Key': self.api_key}
    #     response = requests.get(url, headers=headers)
    #     return response.json()
    
    # def get_book(self, title: str) -> dict:
    #     url = f'{self.base_url}{self.bin_id}'
    #     headers = {'X-Access-Key': self.api_key}
    #     response = requests.get(url, headers=headers)
    #     response.raise_for_status()

    #     data = response.json()['record']
    #     for book in data:
    #         if book['title'] == title:
    #             return book

    #     raise HTTPException(status_code=404, detail='Book not found')


    def get(self, title: str = None) -> dict:
        '''Получение книги'''
        raise NotImplementedError('GET не требуется, обрабатываем через БД')

        # url = f'{self.base_url}{self.bin_id}'
        # headers = {'X-Access-Key': self.api_key}
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()
        # data = response.json()['record']

        # if title:
        #     for book in data:
        #         if book['title'] == title:
        #             return book
        #     raise HTTPException(status_code=404, detail='Book not found')

        # return data
    
    def post(self, book: dict) -> dict:
        '''Добавление книги'''
        return self.add_book(book)
    
    def put(self, book: dict) -> dict:
        '''Обновление книги'''
        return self.update_book(book)
    
    def add_book(self, book: dict) -> dict:
        '''Добавление книги'''
        logger.info(f'Добавление книги в облако: {book}')

        get_url = f'{self.base_url}{self.bin_id}/latest'
        headers = {
            'X-Master-Key': '$2a$10$VTBr0cpzUWdfTIfyl3Rb5u60I6TjkpAlesONyjYW6YoDpu1jlSbGe',  # именно Master-Key для записи
            'Content-Type': 'application/json'
        }
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']

        if any(b['id'] == book['id'] for b in data):
            raise HTTPException(status_code=400, detail='Книга уже существует')
        
        ol_client = OpenLibraryAPI()
        extra = ol_client.get(title=book['title'], author=book['author'])

        book['description'] = extra.get('description')
        book['cover_url'] = extra.get('cover_url')
        
        if not book.get('year') and extra.get('first_publish_year'):
            book['year'] = extra['first_publish_year']

        logger.info(f'Добавляем книгу в облако: {book}')
        data.append(book)

        put_url = f'{self.base_url}{self.bin_id}'
        response = requests.put(put_url, headers=headers, json=data)
        response.raise_for_status()
        return book
    
    def update_book(self, book: dict) -> dict:
        get_url = f'{self.base_url}{self.bin_id}/latest'
        headers = {
            'X-Master-Key': '$2a$10$VTBr0cpzUWdfTIfyl3Rb5u60I6TjkpAlesONyjYW6YoDpu1jlSbGe',  
            'Content-Type': 'application/json'
        }
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']

        for i, b in enumerate(data):
            if b['id'] == book['id']:
                data[i] = book
                break

        put_url = f'{self.base_url}{self.bin_id}'
        response = requests.put(put_url, headers=headers, json=data)
        response.raise_for_status()
        return book
    
    def delete(self, book_id: int) -> dict:
        get_url = f'{self.base_url}{self.bin_id}/latest'
        headers = {
            'X-Master-Key': '$2a$10$VTBr0cpzUWdfTIfyl3Rb5u60I6TjkpAlesONyjYW6YoDpu1jlSbGe',  
            'Content-Type': 'application/json'
        }
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']

        for i, b in enumerate(data):
            if b['id'] == book_id:
                del data[i]
                break

        put_url = f'{self.base_url}{self.bin_id}'
        response = requests.put(put_url, headers=headers, json=data)
        response.raise_for_status()
        return data