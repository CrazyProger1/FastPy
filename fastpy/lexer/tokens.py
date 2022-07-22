from abc import ABC, abstractmethod
from .token_types import TokenTypes
from fastpy.import_tools import import_class
from .config import *


class BaseToken(ABC):
    @property
    @abstractmethod
    def type(self) -> TokenTypes: ...

    @property
    @abstractmethod
    def text(self) -> str: ...

    @property
    @abstractmethod
    def line(self) -> int: ...

    @property
    @abstractmethod
    def name(self) -> str: ...


class Token(BaseToken):
    def __init__(self, token_type: TokenTypes, text: str, line: int, name: str = None):
        self._type = token_type
        self._text = text
        self._line = line
        self._name = name

    @property
    def type(self) -> TokenTypes:
        return self._type

    @property
    def text(self) -> str:
        return self._text

    @property
    def line(self) -> int:
        return self._line

    @property
    def name(self) -> str | None:
        return self._name

    def __repr__(self):
        return f'{self._text}({self._type.name})'


def code_from_tokens(tokens: list[BaseToken] | tuple[BaseToken]):
    code = ''
    for token in tokens:
        code += token.text
    return code


_token_class: BaseToken | None = None


def create_token(token_type: TokenTypes, text: str, line: int, name: str = None, **kwargs) -> BaseToken:
    """Token factory"""
    global _token_class

    if not _token_class:
        _token_class = import_class(TOKEN_CLASS_PATH)

    return _token_class(token_type, text, line, name, **kwargs)
