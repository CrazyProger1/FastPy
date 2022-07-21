from .token import Token
from ..exceptions import *
from ..log import Logger
from .config import *
import re


class Lexer:
    def __init__(self, code: str):
        self._code = code
        self._tokens: list[Token] = []

    @Logger.info_decorator(pattern='Lexing: {line_number}: {code_line}')
    def lex_line(self, code_line: str, line_number: int):
        pass

    @Logger.info_decorator('Start lexing...')
    def lex(self) -> list[Token]:
        for i, code_line in enumerate(self._code.split('\n')):
            if code_line == '' or code_line.startswith(COMMENT_START_SYMBOL):
                continue

            self.lex_line(
                code_line=code_line,
                line_number=i + 1
            )

        return self._tokens
