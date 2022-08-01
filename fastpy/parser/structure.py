from .nodes import *


class Structure:
    """
    Contains information about currently detected structure, such as if condition or function
    """

    def __init__(self, node, level: int = 0):
        self._level = level
        self._node: NodeWithBody = node

    def push_node(self, node: BaseNode):
        self._node.push_node_to_body(node=node)

    def within_struct(self, level: int):
        return level == self._level

    def __repr__(self):
        return str(self._node)
