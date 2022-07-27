from abc import abstractmethod, ABC
from .config import *
from ..import_tools import import_class
from ..module import Module
from ..parser import BaseAST, BaseNode
from ..log import Logger
from .node_transpilers import *
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
        self._internal_code = ''
        self._external_code = ''
        self._transpilers = {}

        self._load_template()
        self._load_transpilers()

    def _load_transpilers(self):
        for node_class_path, transpiler_class_path in NODE_TRANSPILING.items():
            self._transpilers.update({
                import_class(node_class_path): import_class(transpiler_class_path)()
            })

    def _load_template(self):
        env = Environment(
            loader=FileSystemLoader(CPP_TEMPLATES_DIR)
        )

        if self._current_module.name == '__main__':
            self._code_template = env.get_template(CPP_MAIN_TEMPLATE_PATH)

    def _transpile_node(self, node: BaseNode) -> Code:
        Logger.log_info(f'Transpiling: {node.line}: {node}')
        transpiler: BaseNodeTranspiler = self._transpilers.get(node.__class__)
        return transpiler.transpile(
            node=node,
            transpile_node_clb=self._transpile_node
        )

    @Logger.info('Start transpiling...', ending_message='Transpiling completed in {time}')
    def transpile(self) -> str:
        for node in self._ast.nodes(self._current_module.name):
            code = self._transpile_node(
                node=node
            )
            self._internal_code += code.internal + '\n'
            self._external_code += code.external + '\n'

        return self._code_template.render(
            external_code=self._external_code,
            internal_code=self._internal_code
        )


def create_transpiler(module: Module, ast: BaseAST) -> BaseTranspiler:
    """Transpiler factory"""
    return import_class(TRANSPILER_CLASS_PATH)(
        module=module,
        ast=ast
    )
