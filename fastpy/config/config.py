from abc import ABC, abstractmethod


class Config(ABC):
    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def save(self) -> None: ...
