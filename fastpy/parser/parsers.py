from abc import ABC, abstractmethod
from ..lexer import BaseToken, TokenTypes
from .ast import BaseAST, create_ast
from .config import *
from ..import_tools import import_class
from ..log import Logger
from .nodes import *
from .structure import *


class BaseParser(ABC):
    @abstractmethod
    def __init__(self, tokens: list[BaseToken]): ...

    @abstractmethod
    def parse(self) -> BaseAST: ...


class Parser(BaseParser):
    def __init__(self, tokens: list[BaseToken]):
        self._tokens = tokens
        self._ast = create_ast()
        self._structures: list[Structure] = []
        self._current_structure: Structure | None = None

    def _parse_node(self, tokens: list[BaseToken]) -> BaseNode | None:
        pass

    def _detect_struct_start(self, node: BaseNode, level: int):
        if isinstance(node, NodeWithBody):
            self._current_structure = Structure(
                node=node,
                level=level
            )
            self._structures.append(self._current_structure)
            Logger.log_info('Structure detected:', node, ': level:', level)

    @Logger.info_decorator(pattern='Parsing: {expr_tokens[0].line}: {expr_tokens}: level: {expr_level}')
    def _parse_expression(self, expr_tokens: list[BaseToken], expr_level: int):
        node = self._parse_node(expr_tokens)

        if node:
            self._detect_struct_start(node=node, level=expr_level)
            if self._current_structure and self._current_structure.within_struct(expr_level):
                self._current_structure.push_node(node)
            else:
                if self._current_structure and len(self._structures) >= 2:
                    self._structures.pop(-1)
                    self._current_structure = self._structures[-1]
                else:
                    self._current_structure = None
                    self._structures.clear()

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
