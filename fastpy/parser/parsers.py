from abc import ABC, abstractmethod
from ..lexer import BaseToken, TokenTypes
from .ast import BaseAST, create_ast
from .config import *
from ..import_tools import import_class
from ..log import Logger


class BaseParser(ABC):
    @abstractmethod
    def __init__(self, tokens: list[BaseToken]): ...

    @abstractmethod
    def parse(self) -> BaseAST: ...


class Parser(BaseParser):
    def __init__(self, tokens: list[BaseToken]):
        self._tokens = tokens
        self._ast = create_ast()

    def _parse_node(self, tokens: list[BaseToken]):
        pass

    @Logger.info_decorator(pattern='Parsing: {expr_tokens[0].line}: {expr_tokens}: level: {expr_level}')
    def _parse_expression(self, expr_tokens: list[BaseToken], expr_level: int):
        pass

    @Logger.info_decorator('Start parsing...', ending_message='Parsing completed in {time}')
    def parse(self) -> BaseAST:
        expr_tokens = []
        expr_level = 0
        code_started = False

        for token in self._tokens:

            if token.type in [TokenTypes.gap]:
                if not code_started:
                    expr_level += 1
                continue

            elif token.type in [TokenTypes.tab]:
                if not code_started:
                    expr_level += 4
                continue

            elif token.type in [TokenTypes.endline]:
                self._parse_expression(expr_tokens=expr_tokens, expr_level=expr_level)
                expr_tokens.clear()
                expr_level = 0
                code_started = False
                continue

            code_started = True
            expr_tokens.append(token)

        return self._ast


def create_parser(tokens: list[BaseToken]) -> BaseParser:
    """Parser factory"""

    return import_class(PARSER_CLASS_PATH)(tokens)
