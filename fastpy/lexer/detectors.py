from abc import ABC, abstractmethod
from .tokens import BaseToken, create_token
from .token_types import TokenTypes
import re


class BaseDetector(ABC):
    @abstractmethod
    def detect(self,
               code_line: str,
               line_number: int,
               column_number: int,
               regex_pattern: str,
               supposed_token_type: TokenTypes) -> BaseToken: ...


class LiteralDetector(BaseDetector):
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
