from abc import ABC, abstractmethod
from ..lexer import BaseToken, TokenTypes, code_from_tokens
from ..module import Module
from ..import_tools import import_class
from .config import *
from .ast import *
from ..exceptions import ParsingError
from ..log import Logger
from .structure import *
from .node_parsers import *


class BaseParser(ABC):
    """Parser interface"""

    @abstractmethod
    def __init__(self,
                 module: Module,
                 tokens: list[BaseToken]): ...

    @abstractmethod
    def parse(self) -> BaseAST:
        """Parses tokens and returns an Abstract Syntax Tree"""


class Parser(BaseParser):
    """Basic parser of FastPy"""

    @Logger.info(pattern='Parser created ({module})')
    def __init__(self,
                 module: Module,
                 tokens: list[BaseToken]):
        self._ast = create_ast()
        self._current_module = module
        self._current_struct: Structure | None = None
        self._structs: list[Structure] = []
        self._tokens = tokens
        self._node_parsers = {}
        self._load_parsers()

    def _load_parsers(self):
        for node_name, parse_info in NODE_PARSING.items():
            self._node_parsers.update({
                import_class(parse_info.get('node_class')):
                    {
                        'parser_instance': import_class(parse_info.get('parser_class'))(),
                        'cases': parse_info.get('cases')
                    }
            })

    def _parse_node(self, tokens: list[BaseToken],
                    possible_node_types: list[type[BaseNode]] = None,
                    parser: BaseNodeParser = None) -> BaseNode:
        if parser:
            for node_type in possible_node_types:
                cases = self._node_parsers.get(node_type).get('cases')
                for parser_args in cases:
                    if parser.validate(tokens=tokens,
                                       supposed_node_type=node_type,
                                       **parser_args.get('validate_data')):
                        return parser.parse(tokens=tokens,
                                            supposed_node_type=node_type,
                                            parse_node_clb=self._parse_node,
                                            **parser_args.get('parse_data'))

        for node_type, parser_info in self._node_parsers.items():
            parser_instance: BaseNodeParser = parser_info.get('parser_instance')
            cases = parser_info.get('cases')

            if possible_node_types and node_type not in possible_node_types:
                continue

            if node_type not in parser_instance.parses:
                continue

            for parser_args in cases:
                if parser_instance.validate(tokens=tokens,
                                            supposed_node_type=node_type,
                                            **parser_args.get('validate_data')):
                    return parser_instance.parse(tokens=tokens,
                                                 supposed_node_type=node_type,
                                                 parse_node_clb=self._parse_node,
                                                 **parser_args.get('parse_data'))

        raise ParsingError(f'SyntaxError: failed to parse expression "{code_from_tokens(tokens)}"')

    def _detect_struct_start(self, node: BaseNode, level: int):
        if isinstance(node, NodeWithBody):
            self._current_struct = Structure(
                node=node,
                level=level
            )
            self._structs.append(self._current_struct)

    def _within_struct(self, level: int):
        return self._current_struct and self._current_struct.within_struct(level=level)

    @Logger.info(pattern='Parsing: {expr_tokens[0].line}: {expr_tokens}: level: {expr_level}')
    def _parse_expression(self, expr_tokens: list[BaseToken], expr_level: int):
        """Parses each line of code split into tokens"""

        node = self._parse_node(expr_tokens)

        self._detect_struct_start(node, expr_level)

        if self._within_struct(level=expr_level):
            self._current_struct.push_node(node=node)
        else:
            self._ast.push_node(
                module=self._current_module,
                node=node
            )
            if len(self._structs) >= 2:
                self._structs.pop(-1)
                self._current_struct = self._structs[-1]
            else:
                self._current_struct = None

    @Logger.info('Start parsing...', ending_message='Parsing completed in {time}')
    # @Logger.catch_errors()
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
                try:
                    self._parse_expression(
                        expr_tokens=expr_tokens,
                        expr_level=expr_level
                    )
                except ParsingError as e:
                    Logger.log_critical(f'{self._current_module.filepath}: {expr_tokens[0].line}: {e}')
                    os.system('pause')
                    exit(-1)

                expr_tokens.clear()
                expr_level = 0
                code_started = False
                continue

            code_started = True
            expr_tokens.append(token)

        return self._ast


def create_parser(module: Module,
                  tokens: list[BaseToken], ):
    return import_class(PARSER_CLASS_PATH)(module=module, tokens=tokens)
