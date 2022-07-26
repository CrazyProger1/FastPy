from .nodes import *
from .validators import *
from ..singleton import singleton
from ..import_tools import import_class
from ..lexer import TokenTypes, code_from_tokens
from .config import *


class BaseNodeParser(ABC):
    parses: tuple[type[BaseNode]]

    @abstractmethod
    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool: ...

    @abstractmethod
    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BaseNode: ...


@singleton
class UniversalNodeParser(BaseNodeParser):
    parses = (AssignNode,)

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        methods = extra_data.get('methods')
        if not methods:
            return False

        for method_name, method_kwargs in methods.items():
            if not getattr(Validators, method_name)(
                    tokens=tokens,
                    **method_kwargs
            ):
                return False
        return True

    @staticmethod
    def _parse_value(tokens: list[BaseToken], parse_node: callable, **value_data):
        index = value_data.get('index')
        parser_class_path = value_data.get('parser_class')
        nullable = value_data.get('nullable', True)
        value = None

        if index is not None:
            value = tokens[index]

        elif parser_class_path:
            parser_class = import_class(parser_class_path)
            parser = parser_class()
            possible_node_types = tuple(
                import_class(node_class_path)
                for node_class_path in value_data.get('possible_node_classes')
            )
            tokens_slice_data = value_data.get('tokens_slice')
            slice_start = tokens_slice_data.get('start_index')
            if slice_start:
                value = parse_node(
                    tokens=tokens[slice_start::],
                    possible_node_types=possible_node_types,
                    parser=parser
                )
        if not nullable and not value:
            raise ParsingError(value_data.get('error_message'))
        return value

    def parse(self,
              tokens: list[BaseToken],
              supposed_node_type: type[BaseNode],
              parse_node_clb: callable,
              **extra_data) -> BaseNode:
        node_arguments = {}
        for key, value_data in extra_data.items():
            node_arguments.update({
                key: self._parse_value(
                    tokens=tokens,
                    parse_node=parse_node_clb,
                    **value_data)
            })

        return supposed_node_type(
            **node_arguments
        )


@singleton
class BinOpNodeParser(BaseNodeParser):
    parses = (BinOpNode,)

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        left_operand = None

        for token in tokens:
            if not left_operand and token.type in [TokenTypes.identifier, TokenTypes.number]:
                left_operand = token
            elif token.type == TokenTypes.operator \
                    and token.name in BIN_OP_NAMES:
                if left_operand:
                    return True
                return False

    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BinOpNode | tuple[int, BinOpNode]:
        left_operand, right_operand = None, None
        operator = None
        ignore_before = -1
        parenthesis_expected = extra_data.get('parenthesis_expected')

        for i, token in enumerate(tokens):
            if i <= ignore_before:
                continue

            match token.type:
                case TokenTypes.number:
                    if not left_operand:
                        left_operand = ValueNode(token)
                    elif not right_operand:
                        right_operand = ValueNode(token)
                    else:
                        left_operand = BinOpNode(
                            left_operand=left_operand,
                            operator=operator,
                            right_operand=right_operand
                        )
                        right_operand = ValueNode(token)
                        operator = None

                case TokenTypes.identifier:
                    if not left_operand:
                        left_operand = VariableNode(token)
                    elif not right_operand:
                        right_operand = VariableNode(token)
                    else:
                        left_operand = BinOpNode(
                            left_operand=left_operand,
                            operator=operator,
                            right_operand=right_operand
                        )
                        right_operand = VariableNode(token)
                        operator = None

                case TokenTypes.operator:
                    if not operator:
                        operator = token
                    else:
                        left_operand = BinOpNode(
                            left_operand=left_operand,
                            operator=operator,
                            right_operand=right_operand
                        )
                        operator = token
                        right_operand = None

                case TokenTypes.start_parenthesis:
                    checked, operand = self.parse(
                        tokens[i + 1::],
                        parse_node_clb,
                        supposed_node_type,
                        parenthesis_expected=True
                    )
                    if isinstance(operand, BinOpNode):
                        operand.in_brackets = True

                    ignore_before = checked + i

                    if not left_operand:
                        left_operand = operand
                    elif not right_operand:
                        right_operand = operand

                case TokenTypes.end_parenthesis:
                    if parenthesis_expected:
                        if isinstance(left_operand, BinOpNode) and operator is None and right_operand is None:
                            return i + 1, left_operand

                        return i + 1, BinOpNode(
                            left_operand=left_operand,
                            operator=operator,
                            right_operand=right_operand
                        )
        if isinstance(left_operand, BinOpNode) and operator is None and right_operand is None:
            return left_operand

        return BinOpNode(
            left_operand=left_operand,
            operator=operator,
            right_operand=right_operand
        )
