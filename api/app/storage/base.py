from abc import ABC, abstractmethod

class StorageHandler(ABC):
    @abstractmethod
    def save(self, filename: str, data: bytes) -> None:
        pass