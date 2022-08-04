from abc import ABC, abstractmethod
from .tokens import BaseToken, create_token
from .token_types import TokenTypes
from .config import *
from ..exceptions import *
import re
import string


class BaseDetector(ABC):
    """Token detector interface"""

    detects: tuple[TokenTypes]

    @abstractmethod
    def detect(self,
               code: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken:
        """
        Splits a portion of a FastPy code line into a token

        :param code: FastPy source code part
        :param line_number:
        :param column_number:
        :param regex_pattern: regular expression that helps to detect and extract token
        :param supposed_token_type: supposed type of token
        :return: extracted token
        """


class UniversalDetector(BaseDetector):
    """
    Lets to detect and extract several types of token such number & identifier
    """

    detects = (TokenTypes.number, TokenTypes.identifier)

    def detect(self,
               code: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken:
        cut_string = code[column_number::]
        result = re.match(regex_pattern, cut_string)

        if result:
            result_string = result.group().strip()
            return create_token(supposed_token_type, result_string, line_number)


class LiteralDetector(BaseDetector):
    """
    Lets to detect and extract token of string literal type
    """
    detects = (TokenTypes.literal,)

    @staticmethod
    def _escape_double_quote(literal: str) -> str:
        out_literal = ''

        for char in literal[1:-1]:
            match char:
                case '\\':
                    pass
                case '"':
                    out_literal += '\\"'
                case _:
                    out_literal += char
        return '"' + out_literal + '"'

    @staticmethod
    def _extract_string_literal(code: str, pattern: str) -> str:
        start = code[0]

        result = re.search(pattern, code)
        literal = None
        if result:
            literal = result.group()

            if literal.count(start) > 2:
                ignore_next = False
                for i, char in enumerate(literal[1::]):
                    if ignore_next:
                        ignore_next = False
                        continue

                    if char == '\\':
                        ignore_next = True
                    if char == start:
                        return '"' + literal[1:i + 1] + '"'

        return ('"' + literal[1:-1] + '"') if literal else None

    def detect(self,
               code: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken | None:
        cut_string = code[column_number::]

        if cut_string[0] not in ['"', "'"]:
            return

        string_literal = self._extract_string_literal(
            code=cut_string,
            pattern=regex_pattern
        )
        if not string_literal:
            return

        return create_token(
            token_type=supposed_token_type,
            text=self._escape_double_quote(string_literal),
            line=line_number,
        )


class OperatorDetector(BaseDetector):
    """
    Lets to detect and extract token of operator type
    """

    detects = (TokenTypes.operator,)

    def detect(self,
               code: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken:

        cut_string = code[column_number::]

        start = cut_string[0]

        overlaps = []

        for op, name in OPERATORS.items():
            if start == op[0]:
                if op[0] in string.ascii_letters and name != 'else':
                    if re.match(op + ' ', cut_string):
                        overlaps.append(op)
                else:

                    if re.match(re.escape(op), cut_string):
                        overlaps.append(op)

        if len(overlaps) > 0:
            overlaps.sort(key=len)
            return create_token(
                supposed_token_type,
                overlaps[-1],
                line_number,
                OPERATORS.get(overlaps[-1])
            )
