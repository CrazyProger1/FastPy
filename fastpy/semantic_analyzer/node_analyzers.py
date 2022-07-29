from abc import ABC, abstractmethod
from ..singleton import singleton
from ..parser.nodes import *
from ..parser import BaseAST
from ..module import Module
from .scope import *
from ..exceptions import *
from .config import *


class BaseNodeAnalyzer(ABC):
    @abstractmethod
    def analyze(self,
                node: BaseNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope): ...


@singleton
class AssignNodeAnalyzer(BaseNodeAnalyzer):
    def analyze(self,
                node: AssignNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope):

        if not scope.already_defined(node.identifier.text):
            node.definition = True
        else:
            node.definition = False


@singleton
class FuncNodeAnalyzer(BaseNodeAnalyzer):
    @staticmethod
    def _analyze_args(arguments: list[AssignNode], analyze_node_clb: callable):
        for arg_node in arguments:
            analyze_node_clb(arg_node)

    @staticmethod
    def _analyze_body(body: list[BaseNode], analyze_node_clb: callable):
        for body_node in body:
            analyze_node_clb(body_node)

    def analyze(self,
                node: FuncNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope):

        if scope.already_defined(node.identifier.text):
            raise AnalyzingError(f'SemanticError: function with name "{node.identifier.text}" already defined')

        scope.push(node)
        self._analyze_args(node.arguments, analyze_node_clb)
        self._analyze_body(node.body, analyze_node_clb)


@singleton
class IfNodeAnalyzer(BaseNodeAnalyzer):

    @staticmethod
    def _analyze_body(body: list[BaseNode], analyze_node_clb: callable):
        for body_node in body:
            analyze_node_clb(body_node)

    def analyze(self,
                node: IfNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope):
        self._analyze_body(node.body, analyze_node_clb)


@singleton
class CallNodeAnalyzer(BaseNodeAnalyzer):
    @staticmethod
    def _analyze_args(arguments: list[BaseNode], analyze_node_clb: callable):
        for arg_node in arguments:
            analyze_node_clb(arg_node)

    def analyze(self,
                node: CallNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope):
        self._analyze_args(node.arguments, analyze_node_clb)

        if not scope.already_defined(node.identifier.text):
            raise AnalyzingError(f'SemanticError: function with name "{node.identifier.text}" does not exists')


class WhileNodeAnalyzer(BaseNodeAnalyzer):
    def _analyze_condition(self):
        pass

    @staticmethod
    def _analyze_body(body: list[BaseNode], analyze_node_clb: callable):
        for body_node in body:
            analyze_node_clb(body_node)

    def analyze(self,
                node: WhileNode,
                module: Module,
                ast: BaseAST,
                analyze_node_clb: callable,
                scope: Scope):
        self._analyze_body(node.body, analyze_node_clb)
