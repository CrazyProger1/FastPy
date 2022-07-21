from abc import ABC, abstractmethod

CONFIG_FOLDER = 'config'


class Config(ABC):
    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def save(self) -> None: ...
