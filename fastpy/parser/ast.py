from abc import ABC, abstractmethod


class BaseAST(ABC):
    pass


class AST(BaseAST):
    pass


def create_ast() -> BaseAST:
    """AST factory"""
