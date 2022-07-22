from .nodes import *


class Structure:
    def __init__(self, node, level: int):
        self._level = level
        self._node: NodeWithBody = node

    def push_node(self, node: BaseNode):
        self._node.push_node_to_body(node=node)

    def within_struct(self, level: int):
        return level == self._level
