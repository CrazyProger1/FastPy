from abc import abstractmethod, ABC
from .config import *
from ..import_tools import import_class
from ..module import Module
from ..parser import BaseAST, BaseNode
from ..log import Logger
from jinja2 import Environment, FileSystemLoader, Template


class BaseTranspiler(ABC):
    """Transpailer interface"""

    @abstractmethod
    def __init__(self, module: Module, ast: BaseAST): ...

    @abstractmethod
    def transpile(self) -> str:
        """Transpile an Abstract Syntax Tree to source C++ code"""


class Transpiler(BaseTranspiler):
    """Basic transpailer of FastPy"""

    @Logger.info(pattern='Transpiler created ({module})')
    def __init__(self, module: Module, ast: BaseAST):
        self._current_module = module
        self._ast = ast
        self._code_template: Template | None = None
        self._load_template()

    def _load_template(self):
        env = Environment(
            loader=FileSystemLoader(CPP_TEMPLATES_DIR)
        )

        if self._current_module.name == '__main__':
            self._code_template = env.get_template(CPP_MAIN_TEMPLATE_PATH)

    def _transpile_node(self, node: BaseNode):
        print(node)

    @Logger.info('Start transpiling...', ending_message='Transpiling completed in {time}')
    def transpile(self) -> str:
        for node in self._ast.nodes(self._current_module.name):
            self._transpile_node(node=node)

        return self._code_template.render()


def create_transpiler(module: Module, ast: BaseAST) -> BaseTranspiler:
    """Transpiler factory"""
    return import_class(TRANSPILER_CLASS_PATH)(
        module=module,
        ast=ast
    )
