from abc import ABC, abstractmethod


class IModel(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, filters=None):
        pass

    @abstractmethod
    def update(self, update_data, filters):
        pass

    @abstractmethod
    def delete(self, filters):
        pass
