from abc import ABC, abstractmethod

class BaseApiClient(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    