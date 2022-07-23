from abc import ABC, abstractmethod
from .tokens import BaseToken, create_token
from .token_types import TokenTypes
from .config import *
import re
import string


class BaseDetector(ABC):
    detects: tuple[TokenTypes]

    @abstractmethod
    def detect(self,
               code_line: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken: ...


class UniversalDetector(BaseDetector):
    detects = (TokenTypes.literal, TokenTypes.number, TokenTypes.identifier)

    def detect(self,
               code_line: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken:
        cut_string = code_line[column_number::]
        result = re.match(regex_pattern, cut_string)

        if result:
            result_string = result.group().strip()
            return create_token(supposed_token_type, result_string, line_number)


class OperatorDetector(BaseDetector):
    detects = (TokenTypes.operator,)

    def detect(self,
               code_line: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken:  # test variant, to refactor!!

        cut_string = code_line[column_number::]

        start = cut_string[0]

        overlaps = []

        for op, name in OPERATORS.items():
            if start == op[0]:
                if op[0] in string.ascii_letters:
                    if re.match(op + ' ', cut_string):
                        overlaps.append(op)
                else:
                    if re.match(op, cut_string):
                        overlaps.append(op)

        if len(overlaps) > 0:
            overlaps.sort(key=len)
            return create_token(
                supposed_token_type,
                overlaps[-1],
                line_number,
                OPERATORS.get(overlaps[-1])
            )
