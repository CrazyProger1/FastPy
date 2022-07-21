from .token_types import *

SPECIAL_SYMBOLS = {
    '(': TokenTypes.start_parenthesis,
    ')': TokenTypes.end_parenthesis,
    '[': TokenTypes.start_square,
    ']': TokenTypes.end_square,
    '{': TokenTypes.start_braces,
    '}': TokenTypes.end_braces,
    ' ': TokenTypes.gap,
    '\t': TokenTypes.tab,
    ',': TokenTypes.comma
}
