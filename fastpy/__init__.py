"""This module provides a set of tools for development on FastPy lang."""

import fastpy.config
import fastpy.exceptions
import fastpy.log
import fastpy.lexer
import fastpy.transpiler
import fastpy.semantic_analyzer
from fastpy.dev_kit import *

__all__ = [
    'config',
    'log',
    'exceptions',
    'TranspileAPI',
]
