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
                 ast: BaseAST): ...

    @abstractmethod
    def analyze(self) -> None:
        """Parses tokens and returns an Abstract Syntax Tree"""


class Analyzer(BaseAnalyzer):
    """Basic Analyzer of FastPy"""

    def __init__(self,
                 module: Module,
                 ast: BaseAST):
        self._current_module = module
        self._ast = ast
        self._analyzers = {}
        self._current_scope: Scope | None = None
        self._load_node_analyzers()

    def _load_node_analyzers(self):
        for node_class_path, analyzer_class_path in NODE_ANALYZING.items():
            self._analyzers.update({
                import_class(node_class_path): import_class(analyzer_class_path)()
            })

    def _analyze_node(self, node: BaseNode):
        Logger.log_info(f'Analyzing: {node.line}: {node}')

        analyzer: BaseNodeAnalyzer = self._analyzers.get(node.__class__)

        if analyzer:
            analyzer.analyze(
                node=node,
                module=self._current_module,
                ast=self._ast,
                analyze_node_clb=self._analyze_node,
                scope=self._current_scope
            )

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
