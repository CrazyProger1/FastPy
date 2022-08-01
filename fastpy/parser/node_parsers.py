from .nodes import *
from .validators import *
from ..singleton import singleton
from ..import_tools import import_class
from ..lexer import TokenTypes, code_from_tokens
from .config import *


class BaseNodeParser(ABC):
    """Node Parser interface"""

    parses: tuple[type[BaseNode]]

    @abstractmethod
    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        """
        Validates tokens and returns whether the parser is ready to parse the provided tokens

        :param tokens: tokens to parse
        :param supposed_node_type: supposed type of node
        :param extra_data: data that helps to validate and parse tokens,
         can be loaded from config or transmitted from another node parser
        :return: parser readiness
        """

    @abstractmethod
    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BaseNode | list[BaseNode]:
        """
        Parses tokens and returns one or more obtained nodes.
        Should only run when the validate method returns True

        :param tokens: tokens to parse
        :param parse_node_clb: callback that can be useful to the parser to parse subnodes
        :param supposed_node_type: supposed type of node
        :param extra_data: data that helps to validate and parse tokens,
         can be loaded from config or transmitted from another node parser
        :return:
        """


@singleton
class UniversalNodeParser(BaseNodeParser):
    parses = (
        AssignNode,
        FuncNode,
        CallNode,
        ValueNode,
        VariableNode,
        IfNode,
        ElseNode,
        WhileNode,
        ReturnNode
    )

    @staticmethod
    def _raise_exception(tokens: list[BaseToken], exception_data: dict):
        message = exception_data.get('message')
        raise ParsingError(message + f' "{code_from_tokens(tokens)}"')

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:

        methods = extra_data.get('methods')
        if not methods:
            return False

        for method_name, method_kwargs in methods.items():
            exception = method_kwargs.get('exception')
            if exception:
                method_kwargs.pop('exception')

            if not getattr(Validators, method_name)(
                    tokens=tokens,
                    **method_kwargs
            ):
                if exception:
                    self._raise_exception(tokens=tokens, exception_data=exception)

                return False

        return True

    @staticmethod
    def _parse_value(tokens: list[BaseToken], parse_node: callable, **value_data):
        index = value_data.get('index')
        parser_class_path = value_data.get('parser_class')
        nullable = value_data.get('nullable', True)
        value = value_data.get('value')
        if value:
            return value

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
            slice_end = tokens_slice_data.get('end_index')

            if slice_start:
                value = parse_node(
                    tokens=tokens[slice_start::] if slice_end is None else tokens[slice_start:slice_end],
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
class OperationNodeParser(BaseNodeParser):
    parses = (BinOpNode, LogicOpNode)

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        if supposed_node_type is LogicOpNode:
            if len(tokens) == 1 and tokens[0].type == TokenTypes.identifier:
                return True

            for token in tokens:
                if token.type == TokenTypes.operator and token.name in ['and', 'or', 'not']:
                    return True

        elif supposed_node_type is BinOpNode:
            left_operand = None

            for token in tokens:
                if not left_operand and token.type in [TokenTypes.identifier, TokenTypes.number, TokenTypes.literal]:
                    left_operand = token
                elif token.type == TokenTypes.operator \
                        and token.name in BIN_OP_NAMES:
                    if left_operand:
                        return True
                    return False

    @staticmethod
    def _check_operand_fields(operand: BinOpNode) -> bool:
        if isinstance(operand, BinOpNode):
            return not any((
                operand.right_operand is None,
                operand.left_operand is None,
                operand.operator is None
            ))
        return True

    @staticmethod
    def _create_op_node(left_operand: BaseNode, operator: BaseToken, right_operand: BaseNode):
        if not operator:
            return LogicOpNode(
                left_operand=left_operand,
                operator=operator,
                right_operand=right_operand
            )
        if operator.name in ['and', 'or']:
            return LogicOpNode(
                left_operand=left_operand,
                operator=operator,
                right_operand=right_operand
            )
        else:
            return BinOpNode(
                left_operand=left_operand,
                operator=operator,
                right_operand=right_operand
            )

    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BinOpNode | tuple[int, BinOpNode] | LogicOpNode | tuple[int, LogicOpNode]:
        if len(tokens) == 1 and tokens[0].type == TokenTypes.identifier:
            return LogicOpNode(VariableNode(tokens[0]))

        left_operand, right_operand = None, None
        operator = None
        ignore_before = -1
        parenthesis_expected = extra_data.get('parenthesis_expected')

        for i, token in enumerate(tokens):
            if i <= ignore_before:
                continue

            match token.type:
                case TokenTypes.number | TokenTypes.literal:
                    if not left_operand:
                        left_operand = ValueNode(token)
                    elif not right_operand:
                        right_operand = ValueNode(token)
                    else:
                        left_operand = self._create_op_node(
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
                        left_operand = self._create_op_node(
                            left_operand=left_operand,
                            operator=operator,
                            right_operand=right_operand
                        )
                        right_operand = VariableNode(token)
                        operator = None

                case TokenTypes.operator:
                    if token.name not in BIN_OP_NAMES + LOGIC_OP_NAMES:
                        break
                    if not operator:
                        operator = token
                    else:
                        left_operand = self._create_op_node(
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
                    if isinstance(operand, (BinOpNode, LogicOpNode)):
                        operand.in_brackets = True

                    ignore_before = checked + i

                    if not left_operand:
                        left_operand = operand
                    elif not right_operand:
                        right_operand = operand

                case TokenTypes.end_parenthesis:
                    if parenthesis_expected:
                        parenthesis_expected = False
                        if isinstance(left_operand,
                                      (BinOpNode, LogicOpNode)) and operator is None and right_operand is None:
                            return i + 1, left_operand

                        return i + 1, self._create_op_node(
                            left_operand=left_operand,
                            operator=operator,
                            right_operand=right_operand
                        )
                    else:
                        raise ParsingError(f'SyntaxError: excess closing bracket "{code_from_tokens(tokens)}"')

        if parenthesis_expected:
            raise ParsingError(f'SyntaxError: close bracket expected')

        if not self._check_operand_fields(right_operand) or not self._check_operand_fields(left_operand):
            raise ParsingError(f'SyntaxError: unfinished expression "{code_from_tokens(tokens)}"')

        if isinstance(left_operand, (BinOpNode, LogicOpNode)) and operator is None and right_operand is None:
            return left_operand

        if operator and not right_operand or not operator and right_operand:
            raise ParsingError(f'SyntaxError: failed to parse math expression "{code_from_tokens(tokens)}"')

        return self._create_op_node(
            left_operand=left_operand,
            operator=operator,
            right_operand=right_operand
        )


@singleton
class ArgumentsParser(BaseNodeParser):
    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        return True

    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BaseNode | list[BaseNode]:

        if tokens[0].type == TokenTypes.end_parenthesis:
            return []

        arguments = []
        expr_tokens = []
        opened_parenthesis_counter = 1
        for token in tokens:
            match token.type:
                case TokenTypes.start_parenthesis:
                    opened_parenthesis_counter += 1
                case TokenTypes.end_parenthesis:
                    opened_parenthesis_counter -= 1

                    if opened_parenthesis_counter == 0:
                        node = parse_node_clb(expr_tokens)
                        arguments.append(node)
                        return arguments
                case TokenTypes.comma:
                    if opened_parenthesis_counter == 1:
                        node = parse_node_clb(expr_tokens)
                        arguments.append(node)
                        expr_tokens.clear()
                        continue

            expr_tokens.append(token)


@singleton
class ConditionParser(BaseNodeParser):
    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        return True

    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BaseNode | list[BaseNode]:
        return parse_node_clb(
            tokens[0:-1],
            (LogicOpNode, BinOpNode),
            OperationNodeParser()
        )
