from abc import ABC, abstractmethod
from ..lexer import BaseToken
from ..exceptions import *
import os


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


class PrintableNode(BaseNode, ABC):
    def __repr__(self):
        text = '('
        for attr_name, attr_value in vars(self).items():
            text += f'{attr_name}:{attr_value}, '
        text += ')'
        return self.__class__.__name__ + text


class VariableNode(BasicNode, PrintableNode):
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


class AssignNode(BasicNode, PrintableNode):
    def __init__(self,
                 identifier: BaseToken,
                 value_type: BaseToken = None,
                 value: BaseNode = None):
        self.identifier = identifier
        self.value_type = value_type
        self.value = value

    @property
    def line(self) -> int:
        return self.identifier.line


class FuncNode(NodeWithBody, PrintableNode):
    def __init__(self,
                 identifier: BaseToken,
                 arguments: list[AssignNode] = None,
                 body: list[BaseNode] = None,
                 return_type: BaseToken = None):
        self.identifier = identifier
        self.arguments = arguments or []
        self._body = body or []
        self.return_type = return_type

    @property
    def line(self) -> int:
        return self.identifier.line


class IfNode(NodeWithBody, PrintableNode):
    def __init__(self,
                 condition: list[BaseNode] = None,
                 body: list[BaseNode] = None,
                 elif_cases: list = None,
                 else_body: list[BaseNode] = None):
        self.condition = condition
        self._body = body or []
        self.elif_cases: list[IfNode.__init__] = elif_cases
        self.else_body = else_body

    @property
    def line(self) -> int:
        if not self.condition or len(self.condition) == 0:
            return -1
        return self.condition[0].line


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

    @property
    def line(self) -> int:
        if self.left_operand:
            return self.left_operand.line
        return -1


# class ForNode(BellyNode, PrintableNode):
#     def __init__(self,
#                  body: list[BaseNode] = None,
#                  else_body: list[BaseNode] = None
#                  ):
#         pass


class WhileNode(NodeWithBody, PrintableNode):
    def __init__(self,
                 condition: list[BaseNode] = None,
                 body: list[BaseNode] = None,
                 else_body: list[BaseNode] = None):
        self.condition = condition
        self.else_body = else_body or []
        self.body = body

    @property
    def line(self) -> int:
        if not self.condition or len(self.condition) == 0:
            return -1
        return self.condition[0].line


class ImportNode(BasicNode, PrintableNode):
    def __init__(self, filepath: BaseToken = None, parts: list[BaseToken] = None):
        self.filepath = filepath
        self.parts = parts
        self._check_filepath()

    def _check_filepath(self):
        filepath = self.filepath.text[1:-1]
        if not os.path.exists(filepath):
            raise ParsingError(f'ImportError: module with this name "{filepath}" does not exists')

    @property
    def line(self) -> int:
        if not self.filepath:
            return -1
        return self.filepath.line
