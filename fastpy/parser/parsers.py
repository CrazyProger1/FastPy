from abc import ABC, abstractmethod
from ..lexer import BaseToken, TokenTypes
from .ast import BaseAST, create_ast
from .config import *
from ..import_tools import import_class
from ..log import Logger
from .nodes import *
from .node_parsers import *
from .structure import *


class BaseParser(ABC):
    @abstractmethod
    def __init__(self, tokens: list[BaseToken]): ...

    @abstractmethod
    def parse(self) -> BaseAST:
        """Parses tokens and returns an Abstract Syntax Tree"""


class Parser(BaseParser):
    """Basic parser of FastPy"""

    def __init__(self, tokens: list[BaseToken]):
        self._tokens = tokens
        self._ast = create_ast()
        self._structures: list[Structure] = []
        self._current_structure: Structure | None = None
        self._node_parsers = {}
        self._load_node_parsers()

    def _load_node_parsers(self):
        """Loads parsers, node classes and extra arguments for every node type"""
        for node_name, parsing_info in NODE_PARSING.items():
            self._node_parsers.update({
                node_name: {
                    'node_class': import_class(parsing_info.get('node_class')),

                    'parser_instance': import_class(parsing_info.get('parser_class'))(),
                    # Here parser instance is creating

                    'cases': parsing_info.get('cases')
                }
            })

    def _parse_node(self, tokens: list[BaseToken], possible_nodes: tuple[BaseNode] = None) -> BaseNode | None:
        """Looks through each node type, finds the parser, and parses the node"""
        for node_name, parsing_info in self._node_parsers.items():

            parser: BaseNodeParser = parsing_info.get('parser_instance')
            node_class: type[BaseNode] = parsing_info.get('node_class')

            if node_class not in parser.parses or possible_nodes and node_class not in possible_nodes:
                continue

            cases: list = parsing_info.get('cases')  # additional arguments to be passed to the parser

            for data in cases:
                if parser.validate(tokens, node_class, **data.get('validate_data')):
                    node = parser.parse(
                        tokens=tokens,
                        supposed_node_type=node_class,
                        parse_node_callback=self._parse_node,
                        **data.get('parse_data')
                    )
                    if node:
                        return node

    def _detect_struct_start(self, node: BaseNode, level: int):
        """Checks if a node is the start of a structure and creates the structure"""
        if isinstance(node, NodeWithBody):
            self._current_structure = Structure(
                node=node,
                level=level
            )
            self._structures.append(self._current_structure)
            Logger.log_info('Structure detected:', node, ': level:', level)

    @Logger.info_decorator(pattern='Parsing: {expr_tokens[0].line}: {expr_tokens}: level: {expr_level}')
    def _parse_expression(self, expr_tokens: list[BaseToken], expr_level: int):
        """Parses each line of code split into tokens"""
        node = self._parse_node(expr_tokens)

        if node:
            print("DETECTED NODE:", node)
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
