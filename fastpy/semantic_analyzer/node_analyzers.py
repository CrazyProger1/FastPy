from abc import ABC, abstractmethod
from ..singleton import singleton
from ..parser.nodes import *
from ..parser import BaseAST
from ..module import Module
from .scope import *


class BaseNodeAnalyzer(ABC):
    @abstractmethod
    def analyze(self,
                node: BaseNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope): ...


class AssignNodeAnalyzer(BaseNodeAnalyzer):
    def analyze(self,
                node: BaseNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope):
        pass
