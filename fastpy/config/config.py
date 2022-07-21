from abc import ABC, abstractmethod

CONFIG_FOLDER = 'config'


class Config(ABC):
    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def save(self) -> None: ...

    @abstractmethod
    def get(self, key: str | int, default: any) -> any: ...

    @abstractmethod
    def __getitem__(self, item: str | int): ...

    @abstractmethod
    def __iter__(self): ...

    @abstractmethod
    def __repr__(self): ...
