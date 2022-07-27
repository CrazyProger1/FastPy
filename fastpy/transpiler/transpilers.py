from abc import abstractmethod, ABC
from .config import *
from ..import_tools import import_class
from ..module import Module
from ..parser import BaseAST


class BaseTranspiler(ABC):
    """Transpailer interface"""

    @abstractmethod
    def __init__(self, module: Module, ast: BaseAST): ...

    @abstractmethod
    def transpile(self) -> str:
        """Transpile an Abstract Syntax Tree to source C++ code"""


class Transpiler(BaseTranspiler):
    """Basic transpailer of FastPy"""

    def __init__(self, module: Module, ast: BaseAST):
        self._current_module = module
        self._ast = ast

    def transpile(self) -> str:
        pass


def create_transpiler(module: Module) -> BaseTranspiler:
    """Transpiler factory"""
    return import_class(TRANSPILER_CLASS_PATH)(
        module=module
    )
