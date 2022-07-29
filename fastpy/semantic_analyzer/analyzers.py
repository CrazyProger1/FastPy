from abc import ABC, abstractmethod
from ..module import Module
from ..parser import BaseParser, BaseAST
from ..parser.nodes import *
from ..exceptions import *
from .config import *
from ..import_tools import import_class
from ..log import Logger


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

    def _analyze_node(self, node: BaseNode):
        pass

    @Logger.info('Start analyzing...', ending_message='Analysis completed in {time}')
    def analyze(self) -> None:
        print(self._ast)


def create_analyzer(module: Module, ast: BaseAST) -> BaseAnalyzer:
    """Transpiler factory"""
    return import_class(ANALYZER_CLASS_PATH)(
        module=module,
        ast=ast
    )
