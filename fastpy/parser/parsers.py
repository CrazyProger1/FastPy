from abc import ABC, abstractmethod
from ..lexer import BaseToken
from .ast import BaseAST
from .config import *
from ..import_tools import import_class


class BaseParser:
    @abstractmethod
    def __init__(self, tokens: list[BaseToken]): ...

    @abstractmethod
    def parse(self) -> BaseAST: ...


class Parser(BaseParser):
    def __init__(self, tokens: list[BaseToken]):
        self.tokens = tokens

    def parse(self) -> BaseAST:
        pass


def create_parser(tokens: list[BaseToken]) -> BaseParser:
    """Parser factory"""

    return import_class(PARSER_CLASS_PATH)(tokens)
