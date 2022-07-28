from abc import ABC, abstractmethod
from ..parser.nodes import *
from .code import *
from ..singleton import singleton


class BaseNodeTranspiler(ABC):
    @abstractmethod
    def transpile(self,
                  node: BaseNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode: ...


@singleton
class AssignNodeTranspiler(BaseNodeTranspiler):
    def transpile(self, node: AssignNode, transpile_node_clb: callable, **kwargs) -> BaseCode:
        code = Code()
        code.push_internal(
            f'{node.value_type.text if node.value_type is not None else "auto"} '
            f'{node.identifier.text}{" = " if node.value else ""}'
            f'{transpile_node_clb(node=node.value, **kwargs).internal if node.value else ""}',
            **kwargs
        )

        return code


@singleton
class ValueNodeTranspiler(BaseNodeTranspiler):
    def transpile(self,
                  node: ValueNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()

        value = node.value.text
        if isinstance(value, str):
            value = value.replace('"', '\"').replace("'", '"')

        code.push_internal(
            f'{value}',
            **kwargs
        )
        return code


@singleton
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


@singleton
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


@singleton
class FuncNodeTranspiler(BaseNodeTranspiler):

    @staticmethod
    def _transpile_arguments(arguments: list[BaseNode], transpile_node_clb) -> str:
        code = ''

        for i, arg in enumerate(arguments):
            code += transpile_node_clb(arg, endl=False, auto_semicolon=False).internal
            if i <= len(arguments) - 2:
                code += ', '

        return code

    @staticmethod
    def _transpile_body(body: list[BaseNode], transpile_node_clb) -> str:
        code = Code()

        for i, node in enumerate(body):
            code.push_internal(
                transpile_node_clb(node=node, endl=False, auto_semicolon=False).internal,
            )

        return code.internal

    def transpile(self,
                  node: FuncNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        arguments = self._transpile_arguments(node.arguments, transpile_node_clb)
        body = self._transpile_body(node.body, transpile_node_clb)

        return_type = node.return_type.text if node.return_type else 'void'
        func_code = f'{return_type} {node.identifier.text} ({arguments}){{\n{body}\n}}'
        code.push_external(func_code)
        return code


@singleton
class CallNodeTranspiler(BaseNodeTranspiler):
    @staticmethod
    def _transpile_arguments(arguments: list[BaseNode], transpile_node_clb) -> str:
        code = ''

        for i, arg in enumerate(arguments):
            code += transpile_node_clb(arg, endl=False, auto_semicolon=False).internal
            if i <= len(arguments) - 2:
                code += ', '

        return code

    def transpile(self,
                  node: CallNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        code.push_internal(
            f'{node.identifier.text}({self._transpile_arguments(node.arguments, transpile_node_clb)})',
            **kwargs
        )
        return code


@singleton
class LogicOpNodeTranspiler(BaseNodeTranspiler):
    @staticmethod
    def _transpile_operand(operand: BaseNode, transpile_node_clb) -> str | None:
        if not operand:
            return None

        return transpile_node_clb(operand, auto_semicolon=False, endl=False).internal

    def transpile(self,
                  node: LogicOpNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        left_operand = self._transpile_operand(node.left_operand, transpile_node_clb)
        right_operand = self._transpile_operand(node.right_operand, transpile_node_clb)
        if not right_operand:
            code.push_internal(f'{left_operand}', **kwargs)

        return code


@singleton
class IfNodeTranspiler(BaseNodeTranspiler):

    @staticmethod
    def _transpile_condition(node: LogicOpNode, transpile_node_clb) -> str:
        return transpile_node_clb(node, endl=False, auto_semicolon=False).internal

    @staticmethod
    def _transpile_body(body: list[BaseNode], transpile_node_clb) -> str:
        code = Code()

        for i, node in enumerate(body):
            code.push_internal(
                transpile_node_clb(node=node, endl=False, auto_semicolon=False).internal,
            )

        return code.internal

    def transpile(self,
                  node: IfNode,
                  transpile_node_clb: callable,
                  **kwargs) -> BaseCode:
        code = Code()
        condition = self._transpile_condition(node.condition, transpile_node_clb)
        body = self._transpile_body(node.body, transpile_node_clb)

        code.push_internal(f'if ({condition}) {{\n{body}\n}}', auto_semicolon=False, endl=True)
        return code
