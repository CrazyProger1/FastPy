from abc import ABC, abstractmethod
from ..import_tools import import_class
from .config import *
from .nodes import *
from typing import Iterable
from ..module import Module


class BaseAST(ABC):
    @abstractmethod
    def add_module(self, module: Module) -> None: ...

    @abstractmethod
    def push_node(self, module: Module, node: BaseNode) -> None: ...

    @abstractmethod
    def pop_node(self, module: Module, index: int) -> BaseNode: ...

    @abstractmethod
    def remove_node(self, module: Module, node: BaseNode) -> None: ...

    @abstractmethod
    def nodes(self, module_name: str) -> Iterable[BaseNode]: ...


class AST(BaseAST):
    def __init__(self):
        self._tree = {
            '__main__': []
        }

    def add_module(self, module: Module) -> None:
        self._tree.update({module.name: []})

    def push_node(self, module: Module, node: BaseNode):
        if self._tree.get(module.name) is None:
            self._tree.update({module.name: [node]})
            return

        self._tree.get(module.name).append(node)

    def _check_module_existence(self, module_name: str):
        module_nodes_list = self._tree.get(module_name)
        if not module_nodes_list:
            raise ValueError(f'Module with that name "{module_name}" is not exists')

    def pop_node(self, module: Module, index: int) -> BaseNode:
        self._check_module_existence(module.name)
        return self._tree.get(module.name).pop(index)

    def remove_node(self, module: Module, node: BaseNode) -> None:
        self._check_module_existence(module.name)
        self._tree.get(module.name).remove(node)

    def __repr__(self):
        out = ''

        for key, value in self._tree.items():
            out += '\n' + key + ':\n    '
            out += '\n    '.join(map(str, value))

        return out

    def nodes(self, module_name: str) -> Iterable[BaseNode]:
        module_nodes = self._tree.get(module_name)
        if not module_nodes:
            return ()

        for node in module_nodes:
            yield node


_ast_instance = None


def create_ast() -> BaseAST:
    """AST factory"""
    global _ast_instance

    if not _ast_instance:
        _ast_instance = import_class(AST_CLASS_PATH)()

    return _ast_instance
