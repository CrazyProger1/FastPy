from abc import ABC, abstractmethod
from ..parser.nodes import *
from .code import *


class BaseNodeTranspiler(ABC):
    @abstractmethod
    def transpile(self, node: BaseNode, transpile_node_clb: callable) -> Code: ...


class AssignNodeTranspiler(BaseNodeTranspiler):
    def transpile(self, node: AssignNode, transpile_node_clb: callable) -> Code:
        code = Code()
        code.internal = f'{node.value_type.text if node.value_type is not None else "auto"} ' \
                        f'{node.identifier.text}{" = " if node.value else ";"}' \
                        f'{transpile_node_clb(node=node.value).internal if node.value else ""}'
        return code


class ValueNodeTranspiler(BaseNodeTranspiler):
    def transpile(self, node: ValueNode, transpile_node_clb: callable) -> Code:
        code = Code()
        code.internal = f'{node.value.text};'
        return code
