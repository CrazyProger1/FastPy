from abc import ABC, abstractmethod
from ..lexer import BaseToken


class BaseNode(ABC):
    @property
    @abstractmethod
    def line(self) -> int: ...

    @abstractmethod
    def have_body(self) -> bool: ...


class BellyNode(BaseNode, ABC):
    def have_body(self) -> bool:
        return True


class ThinNode(BaseNode, ABC):
    def have_body(self) -> bool:
        return False


class PrintableNode(BaseNode, ABC):
    def __repr__(self):
        text = '('
        for attr_name, attr_value in vars(self):
            text += f'{attr_name}:{attr_value}, '
        text += ')'
        return self.__class__.__name__ + text


class VariableNode(ThinNode, PrintableNode):
    def __init__(self, identifier: BaseToken):
        self.identifier = identifier

    def line(self) -> int:
        return self.identifier.line


class ValueNode(ThinNode, PrintableNode):
    def __init__(self, value: BaseToken):
        self.value = value

    def line(self) -> int:
        return self.value.line


class AssignNode(ThinNode, PrintableNode):
    def __init__(self,
                 identifier: BaseToken,
                 value_type: BaseToken = None,
                 value: BaseNode = None):
        self.identifier = identifier
        self.value_type = value_type
        self.value = value

    def line(self) -> int:
        return self.identifier.line


class FuncNode(BellyNode, PrintableNode):
    def __init__(self,
                 identifier: BaseToken,
                 arguments: list[AssignNode] = None,
                 body: list[BaseNode] = None,
                 return_type: BaseToken = None):
        self.identifier = identifier
        self.arguments = arguments or []
        self.body = body or []
        self.return_type = return_type

    def line(self) -> int:
        return self.identifier.line


class IfNode(BellyNode, PrintableNode):
    def __init__(self,
                 condition: list[BaseNode] = None,
                 body: list[BaseNode] = None,
                 elif_cases: list = None,
                 else_body: list[BaseNode] = None):
        self.condition = condition
        self.body = body or []
        self.elif_cases: list[IfNode.__init__] = elif_cases
        self.else_body = else_body

    def line(self) -> int:
        if not self.condition or len(self.condition) == 0:
            return -1
        return self.condition[0].line


class BinOpNode(ThinNode, PrintableNode):
    def __init__(self,
                 left_operand: BaseNode = None,
                 right_operand: BaseNode = None,
                 operator: BaseToken = None,
                 priority: int = None):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator
        self.priority = priority

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


class WhileNode(BellyNode, PrintableNode):
    def __init__(self,
                 condition: list[BaseNode] = None,
                 body: list[BaseNode] = None,
                 else_body: list[BaseNode] = None):
        self.condition = condition
        self.body = body or []
        self.else_body = else_body or []

    def line(self) -> int:
        if not self.condition or len(self.condition) == 0:
            return -1
        return self.condition[0].line