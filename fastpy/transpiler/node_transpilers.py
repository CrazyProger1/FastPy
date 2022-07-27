from abc import ABC, abstractmethod
from ..parser.nodes import *
from .code import *


class BaseNodeTranspiler(ABC):
    @abstractmethod
    def transpile(self,
                  node: BaseNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode: ...


class AssignNodeTranspiler(BaseNodeTranspiler):
    def transpile(self, node: AssignNode, transpile_node_clb: callable, **kwargs) -> BaseCode:
        code = Code()
        code.push_internal(
            f'{node.value_type.text if node.value_type is not None else "auto"} '
            f'{node.identifier.text}{" = " if node.value else ""}'
            f'{transpile_node_clb(node=node.value).internal if node.value else ""}',
            **kwargs
        )

        return code


class ValueNodeTranspiler(BaseNodeTranspiler):
    def transpile(self,
                  node: ValueNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        code.push_internal(
            f'{node.value.text}',
            **kwargs
        )
        return code


class VariableNodeTranspiler(BaseNodeTranspiler):
    def transpile(self,
                  node: VariableNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        code.push_internal(
            f'{node.identifier.text}',
            **kwargs
        )
        return code


class BinOpNodeTranspiler(BaseNodeTranspiler):
    def transpile(self,
                  node: BinOpNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        left_operand = transpile_node_clb(node.left_operand, auto_semicolon=False, endl=False)
        right_operand = transpile_node_clb(node.right_operand, auto_semicolon=False, endl=False)
        match_expr = f'{left_operand} {node.operator.text} {right_operand}'

        if node.in_brackets:
            match_expr = '(' + match_expr + ')'

        code.push_internal(match_expr, **kwargs)
        return code
