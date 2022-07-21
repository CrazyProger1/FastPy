from .lexer import *
from .token import *
from .config import *
from import_tools import import_class

__all__ = [
    'Lexer',
    'Token',
    'BaseLexer',
    'BaseToken',
    'lex_code'
]


def lex_code(code: str) -> list[BaseToken]:
    return import_class(LEXER_CLASS)(code).lex()
