from abc import ABC, abstractmethod
from ..import_tools import import_class
from .config import *
from .nodes import *
from typing import Iterable


class BaseAST(ABC):
    @abstractmethod
    def add_module(self, module_name: str) -> None: ...

    @abstractmethod
    def push_node(self, module_name: str, node: BaseNode) -> None: ...

    @abstractmethod
    def pop_node(self, module_name: str, index: int) -> BaseNode: ...

    @abstractmethod
    def remove_node(self, module_name: str, node: BaseNode) -> None: ...

    @abstractmethod
    def module_nodes(self, module_name: str) -> Iterable[BaseNode]: ...


class AST(BaseAST):
    def __init__(self):
        self._tree = {
            '__main__': []
        }

    def add_module(self, module_name: str) -> None:
        self._tree.update({module_name: []})

    def push_node(self, module_name: str, node: BaseNode):
        if self._tree.get(module_name) is None:
            self.add_module(module_name)

        return self._tree.get(module_name).append(node)

    def _check_module_existence(self, module_name: str):
        module_nodes_list = self._tree.get(module_name)
        if not module_nodes_list:
            raise ValueError(f'Module with that name "{module_name}" is not exists')

    def pop_node(self, module_name: str, index: int) -> BaseNode:
        self._check_module_existence(module_name)
        return self._tree.get(module_name).pop(index)

    def remove_node(self, module_name: str, node: BaseNode) -> None:
        self._check_module_existence(module_name)
        self._tree.get(module_name).remove(node)

    def __repr__(self):
        out = ''

        for key, value in self._tree.items():
            out += '\n' + key + ':\n    '
            out += '\n    '.join(map(str, value))

        return out

    def module_nodes(self, module_name: str) -> Iterable[BaseNode]:
        for node in self._tree.get(module_name):
            yield node


_ast_instance = None


def create_ast() -> BaseAST:
    """AST factory"""
    global _ast_instance

    if not _ast_instance:
        _ast_instance = import_class(AST_CLASS_PATH)()

    return _ast_instance
