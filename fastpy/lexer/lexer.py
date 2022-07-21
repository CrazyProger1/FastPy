from abc import ABC, abstractmethod
from .token import BaseToken
from ..exceptions import *
from ..log import Logger
from .config import *
from import_tools import import_class
import re


class BaseLexer(ABC):
    @abstractmethod
    def lex(self) -> list[BaseToken]: ...


class Lexer(BaseLexer):
    def __init__(self, code: str):
        self._code = code
        self._tokens: list[BaseToken] = []

    @Logger.info_decorator(pattern='Lexing: {line_number}: {code_line}')
    def _lex_line(self, code_line: str, line_number: int) -> None:
        pass

    @Logger.info_decorator('Start lexing...', ending_message='Lexing complete')
    def lex(self) -> list[BaseToken]:
        for i, code_line in enumerate(self._code.split('\n')):
            if code_line == '' or code_line.startswith(COMMENT_START_SYMBOL):
                continue

            self._lex_line(
                code_line=code_line,
                line_number=i + 1
            )

        return self._tokens


def lex_code(code: str) -> list[BaseToken]:
    return import_class(LEXER_CLASS)(code).lex()
