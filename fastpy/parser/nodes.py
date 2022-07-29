from abc import ABC, abstractmethod
from ..lexer import BaseToken
from ..exceptions import *
from ..filesystem import FileSystem as Fs


class BaseNode(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs): ...

    @property
    @abstractmethod
    def line(self) -> int: ...


class NodeWithBody(BaseNode, ABC):
    body = []

    def push_node_to_body(self, node: BaseNode):
        self.body.append(node)


class BasicNode(BaseNode, ABC):
    pass


class NamedNode(BaseNode, ABC):
    identifier = None


class NodeWithScope(NodeWithBody, NamedNode, ABC):
    identifier = None


class PrintableNode(BaseNode, ABC):
    def __repr__(self):
        text = '<'
        for attr_name, attr_value in vars(self).items():
            text += f'{attr_name}:{attr_value.text if isinstance(attr_value, BaseToken) else attr_value}, '
        text += '>'
        return self.__class__.__name__ + text


class VariableNode(BasicNode, PrintableNode, NamedNode):
    def __init__(self, identifier: BaseToken):
        self.identifier = identifier

    @property
    def line(self) -> int:
        return self.identifier.line


class ValueNode(BasicNode, PrintableNode):
    def __init__(self, value: BaseToken):
        self.value = value

    @property
    def line(self) -> int:
        return self.value.line


class AssignNode(BasicNode, PrintableNode, NamedNode):
    def __init__(self,
                 identifier: BaseToken,
                 value_type: BaseToken = None,
                 value: BaseNode = None):
        self.identifier = identifier
        self.value_type = value_type
        self.value = value
        self.definition = True

    @property
    def line(self) -> int:
        return self.identifier.line


class FuncNode(NodeWithScope, PrintableNode, NamedNode):
    def __init__(self,
                 identifier: BaseToken,
                 arguments: list[AssignNode] = None,
                 body: list[BaseNode] = None,
                 return_type: BaseToken = None,
                 template: bool = False):
        self.identifier = identifier
        self.arguments = arguments or []
        self.body = body or []
        self.return_type = return_type
        self.template = template

    @property
    def line(self) -> int:
        return self.identifier.line


class CallNode(BasicNode, PrintableNode):
    def __init__(self,
                 identifier: BaseToken,
                 arguments: list[BaseNode] = None):
        self.identifier = identifier
        self.arguments = arguments or []

    @property
    def line(self) -> int:
        return self.identifier.line


class LogicOpNode(BasicNode, PrintableNode):
    def __init__(self,
                 left_operand: BaseNode = None,
                 right_operand: BaseNode = None,
                 operator: BaseToken = None):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator
        self.in_brackets = False

    @property
    def line(self) -> int:
        return self.left_operand.line


class ElseNode(NodeWithBody, PrintableNode):
    def __init__(self, body: list[BaseNode] = None, ):
        self.body = body or []

    @property
    def line(self) -> int:
        if len(self.body) > 0:
            return self.body[0].line
        return -1


class BinOpNode(BasicNode, PrintableNode):
    def __init__(self,
                 left_operand: BaseNode = None,
                 right_operand: BaseNode = None,
                 operator: BaseToken = None,
                 priority: int = None):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator
        self.priority = priority
        self.in_brackets = False

    @staticmethod
    def _get_operand_len(operand: BaseNode):
        if isinstance(operand, (VariableNode, ValueNode)):
            return 1
        elif isinstance(operand, BinOpNode):
            return len(operand)
        return 0

    def __len__(self):
        tokens_number = 1
        tokens_number += self._get_operand_len(self.left_operand)
        tokens_number += self._get_operand_len(self.right_operand)
        return tokens_number

    def __repr__(self):
        op_text = f'{self.left_operand} {self.operator.text} {self.right_operand}'
        if self.in_brackets:
            op_text = '( ' + op_text + ' )'

        return self.__class__.__name__ + f'<{op_text}>'

    @property
    def line(self) -> int:
        if self.left_operand:
            return self.left_operand.line
        return -1


class IfNode(NodeWithBody, PrintableNode):
    def __init__(self,
                 condition: LogicOpNode | BinOpNode = None,
                 body: list[BaseNode] = None,
                 elif_cases: list = None,
                 else_case: ElseNode = None,
                 is_elif: bool = False):
        self.condition = condition
        self.body = body or []
        self.elif_cases: list[IfNode.__init__] = elif_cases
        self.else_case = else_case
        self.is_elif = is_elif

    @property
    def line(self) -> int:
        return self.condition.line


# class ForNode(BellyNode, PrintableNode):
#     def __init__(self,
#                  body: list[BaseNode] = None,
#                  else_body: list[BaseNode] = None
#                  ):
#         pass


class WhileNode(NodeWithBody, PrintableNode):
    def __init__(self,
                 condition: LogicOpNode | BinOpNode = None,
                 body: list[BaseNode] = None,
                 else_body: list[BaseNode] = None):
        self.condition = condition
        self.else_body = else_body or []
        self.body = body or []

    @property
    def line(self) -> int:
        if not self.condition or len(self.condition) == 0:
            return -1
        return self.condition.line

# class ImportNode(BasicNode, PrintableNode):
#     def __init__(self, filepath: BaseToken = None, parts: list[BaseToken] = None):
#         self.filepath = filepath
#         self.parts = parts
#
#     @property
#     def line(self) -> int:
#         if not self.filepath:
#             return -1
#         return self.filepath.line
