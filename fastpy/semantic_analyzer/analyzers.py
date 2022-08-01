from abc import ABC, abstractmethod
from ..module import Module
from ..parser import BaseParser, BaseAST
from ..parser.nodes import *
from ..exceptions import *
from .config import *
from ..import_tools import import_class
from ..log import Logger
from .node_analyzers import *
from .scope import *


class BaseAnalyzer(ABC):
    """Parser interface"""

    @abstractmethod
    def __init__(self,
                 module: Module,
                 ast: BaseAST):
        """

        :param module: module: the module parameter contains information about the currently processed file
        :param ast: Abstract Syntax Tree - output of previous parsing stage
        """

    @abstractmethod
    def analyze(self) -> None:
        """Parses tokens and returns an Abstract Syntax Tree"""


class Analyzer(BaseAnalyzer):
    """Basic Analyzer implementation of FastPy"""

    def __init__(self,
                 module: Module,
                 ast: BaseAST):
        self._current_module = module
        self._ast = ast
        self._analyzers = {}
        self._current_scope: Scope | None = Scope()
        self._scopes = [self._current_scope]
        self._load_node_analyzers()

    def _load_node_analyzers(self):
        for node_class_path, analyzer_class_path in NODE_ANALYZING.items():
            self._analyzers.update({
                import_class(node_class_path): import_class(analyzer_class_path)()
            })

    def _detect_scope_start(self, node: BaseNode):
        if isinstance(node, FuncNode):
            global_vars = self._current_scope.get_global()
            self._current_scope = Scope(node)

            self._current_scope.push_several(global_vars)
            self._scopes.append(self._current_scope)

    def _detect_scope_end(self, node: BaseNode):
        if self._current_scope.is_scope_node(node):
            self._scopes.pop(-1)
            self._current_scope = self._scopes[-1]

    def _analyze_node(self, node: BaseNode, **kwargs):
        Logger.log_info(f'Analyzing: {node.line}: {node}')

        self._detect_scope_start(node)

        analyzer: BaseNodeAnalyzer = self._analyzers.get(node.__class__)

        try:
            if analyzer:
                analyzer.analyze(
                    node=node,
                    module=self._current_module,
                    ast=self._ast,
                    analyze_node_clb=self._analyze_node,
                    scope=self._current_scope
                )
        except AnalyzingError as e:
            Logger.log_critical(f'{self._current_module.filepath}: {node.line}: {e}')
            os.system('pause')
            exit(-1)

        self._detect_scope_end(node)

        if isinstance(node, NamedNode):
            self._current_scope.push(node)

    @Logger.info('Start analyzing...', ending_message='Analysis completed in {time}')
    def analyze(self) -> None:
        for node in self._ast.nodes(self._current_module.name):
            self._analyze_node(node)


def create_analyzer(module: Module, ast: BaseAST) -> BaseAnalyzer:
    """Analyzer factory"""
    return import_class(ANALYZER_CLASS_PATH)(
        module=module,
        ast=ast
    )
