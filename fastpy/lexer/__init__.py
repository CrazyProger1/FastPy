"""
This module is responsible for splitting the source code into tokens.
"""

from .lexers import *
from .tokens import *
from .config import *
from .detectors import *

__all__ = [
    'Lexer',
    'Token',
    'BaseLexer',
    'BaseToken',
    'create_lexer',
    'code_from_tokens',
    'create_token',
    'BaseDetector',
    'TokenTypes'
]
