from ..parser.nodes import *
from .config import *


class Scope:
    def __init__(self, node: BaseNode | None = None):
        self._node = node
        self._scope: dict[str, NamedNode] = {}

    def push(self, node: NamedNode):
        self._scope.update({node.identifier.text: node})

    def push_several(self, nodes: list[NamedNode] | tuple[NamedNode]):
        self._scope.update({
            node.identifier.text: node for node in nodes
        })

    def get_global(self):
        for identifier, node in self._scope.items():
            if isinstance(node, FuncNode):
                yield node

    def is_scope_node(self, node: BaseNode):
        return self._node == node

    def already_defined(self, name: str):
        if name in BUILTIN_FUNCTIONS.values() or name in BUILTIN_TYPES.values():
            return True

        return self._scope.get(name) is not None

    def __repr__(self):
        return str(tuple(self._scope.keys()))
