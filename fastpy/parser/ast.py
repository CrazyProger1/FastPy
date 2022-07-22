from abc import ABC, abstractmethod
from ..import_tools import import_class
from .config import *


class BaseAST(ABC):
    pass


class AST(BaseAST):
    pass


def create_ast() -> BaseAST:
    """AST factory"""
    return import_class(AST_CLASS_PATH)()
