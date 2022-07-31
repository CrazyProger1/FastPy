import os
from abc import abstractmethod, ABC
from .config import *
from ..import_tools import import_class
from ..module import Module
from ..parser import BaseAST, BaseNode
from ..log import Logger
from .node_transpilers import *
from jinja2 import Environment, FileSystemLoader, Template
from ..exceptions import *


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
        self._code = Code()
        self._transpilers = {}
        self._additional_includes = Code()

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
        else:
            self._code_template = env.get_template(CPP_TEMPLATE_PATH)

    def _transpile_node(self, node: BaseNode, **kwargs) -> BaseCode:
        Logger.log_info(f'Transpiling: {node.line}: {node}')
        transpiler: BaseNodeTranspiler = self._transpilers.get(node.__class__)
        if not transpiler:
            raise TranspilingError(f'You need to specify the node transpiler for "{node.__class__.__name__}"'
                                   f' in "transpiler.json" config file')

        code = transpiler.transpile(
            node=node,
            transpile_node_clb=self._transpile_node,
            **kwargs
        )


        return code

    def _transpile_import(self, node: CallNode):
        for importing_file in node.arguments:
            if isinstance(importing_file, ValueNode):
                include_path = importing_file.value.text
                include_path = include_path.replace("'", '').replace('"', '')
                include_path = Fs.replace_ext(include_path, '.hpp')
                self._additional_includes.push_external(
                    f'#include "{include_path}"',
                    auto_semicolon=False, endl=True
                )

    @Logger.info('Start transpiling...', ending_message='Transpiling completed in {time}')
    def transpile(self) -> str:
        for node in self._ast.nodes(self._current_module.name):
            if isinstance(node, CallNode) and node.identifier.text == BUILTIN_FUNCTIONS['import']:
                self._transpile_import(node)
                continue

            try:
                code = self._transpile_node(
                    node=node
                )
            except TranspilingError as e:
                Logger.log_critical(f'{self._current_module.filepath}: {node.line}: {e}')
                os.system('pause')
                exit(-1)

            self._code.push_internal(code.internal, auto_semicolon=False)
            self._code.push_external(code.external, auto_semicolon=False)

        return self._code_template.render(
            external_code=self._code.external,
            internal_code=self._code.internal,
            additional_includes=self._additional_includes.external
        )


def create_transpiler(module: Module, ast: BaseAST) -> BaseTranspiler:
    """Transpiler factory"""
    return import_class(TRANSPILER_CLASS_PATH)(
        module=module,
        ast=ast
    )
