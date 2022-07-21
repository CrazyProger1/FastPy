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
               supposed_token_type: TokenTypes) -> BaseToken:

        cut_string = code_line[column_number::]

        start = cut_string[0]
        if start in OPERATORS.keys():
            if start not in SIMILAR_OPERATORS.keys():
                return create_token(
                    token_type=supposed_token_type,
                    text=start,
                    line=line_number,
                    name=OPERATORS.get(start)
                )

        for op in OPERATORS.keys():
            if op.startswith(start):
                if op in string.ascii_letters:
                    result = re.match(op + ' ', cut_string)
                else:
                    result = re.match(op, cut_string)

                if result:
                    return create_token(
                        token_type=supposed_token_type,
                        text=result.group(),
                        line=line_number,
                        name=OPERATORS.get(start)
                    )
