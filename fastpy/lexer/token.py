from abc import ABC, abstractmethod
from .token_types import TokenTypes


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


def code_from_tokens(tokens: list[Token] | tuple[Token]):
    code = ''
    for token in tokens:
        code += token.text
    return code
