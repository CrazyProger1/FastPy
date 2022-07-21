from abc import ABC, abstractmethod
from fastpy.import_tools import import_class
from .special_symbols import *
from .config import *
from .token import BaseToken, create_token
from ..log import Logger


class BaseLexer(ABC):
    @abstractmethod
    def lex(self) -> list[BaseToken]: ...


class Lexer(BaseLexer):
    def __init__(self, code: str):
        self._code = code
        self._tokens: list[BaseToken] = []

    def _discover_token(self, code_line: str, line_number: int, column_number: int) -> int:
        start_symbol = code_line[column_number]

        if start_symbol in SPECIAL_SYMBOLS.keys():
            token_type = SPECIAL_SYMBOLS.get(start_symbol)
            token = create_token(
                token_type=token_type,
                text=start_symbol,
                line=line_number,
            )
            self._tokens.append(token)

        return -1

    @Logger.info_decorator(pattern='Lexing: {line_number}: {code_line}')
    def _lex_line(self, code_line: str, line_number: int) -> None:
        ignore_before = 0
        for column, char in enumerate(code_line):
            if column <= ignore_before:
                continue

            ignore_before = self._discover_token(
                code_line=code_line,
                line_number=line_number,
                column_number=column,
            )

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
