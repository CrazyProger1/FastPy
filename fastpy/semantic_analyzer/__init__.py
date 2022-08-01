"""
This module is responsible for analyzing an Abstract Syntax Tree obtained using the parser.
"""

from .analyzers import *

__all__ = [
    'BaseAnalyzer',
    'create_analyzer'
]
