from abc import ABC, abstractmethod
from fastpy.import_tools import import_class
from .detectors import BaseDetector
from .special_symbols import *
from .config import *
from .tokens import BaseToken, create_token
from ..log import Logger
from ..module import Module
from ..exceptions import *


class BaseLexer(ABC):
    """Lexer interface"""

    @abstractmethod
    def __init__(self, module: Module):
        """

        :param module: the module parameter contains information about the currently processed file.
        """

    @abstractmethod
    def lex(self) -> list[BaseToken]:
        """Splits the code into a list of tokens"""


class Lexer(BaseLexer):
    """Basic lexer implementation of FastPy"""

    @Logger.info(pattern='Lexer created ({module})')
    def __init__(self, module: Module):
        self._current_module = module
        self._code = module.source_code
        self._tokens: list[BaseToken] = []
        self._token_detectors = {
            token_type: import_class(detection_info.get('detector'))()
            for token_type, detection_info in TOKEN_DETECTION.items()
        }

    def _detect_token(self, code_line: str, line_number: int, column_number: int) -> int:
        """Detects and extracts a token from a line of code"""

        start_symbol = code_line[column_number]

        if start_symbol in SPECIAL_SYMBOLS.keys():
            token_type = SPECIAL_SYMBOLS.get(start_symbol)
            token = create_token(
                token_type=token_type,
                text=start_symbol,
                line=line_number,
            )
            self._tokens.append(token)
            return len(token.text) + column_number - 1

        for token_type, detection_info in TOKEN_DETECTION.items():
            supposed_token_type = TokenTypes.__getattr__(token_type)
            detector: BaseDetector = self._token_detectors.get(token_type)

            if supposed_token_type not in detector.detects:
                continue

            regexes = detection_info.get('regexes')

            for regex in regexes:
                token = detector.detect(
                    code=code_line,
                    line_number=line_number,
                    column_number=column_number,
                    regex_pattern=regex,
                    supposed_token_type=supposed_token_type
                )
                if token:
                    self._tokens.append(token)
                    return len(token.text) + column_number - 1

        return -1

    @Logger.info(pattern='Lexing: {line_number}: {code_line}')
    def _lex_line(self, code_line: str, line_number: int) -> None:
        """Splits each line of the code into tokens"""

        ignore_before = -1
        for column, char in enumerate(code_line):
            if char == COMMENT_START_SYMBOL:
                return

            if column <= ignore_before:
                continue

            ignore_before = self._detect_token(
                code_line=code_line,
                line_number=line_number,
                column_number=column,
            )

    @Logger.info('Start lexing...', ending_message='Lexing completed in {time}')
    # @Logger.catch_errors()
    def lex(self) -> list[BaseToken]:
        for i, code_line in enumerate(self._code.split('\n')):
            if code_line == '' or code_line.startswith(COMMENT_START_SYMBOL):
                continue

            try:
                self._lex_line(
                    code_line=code_line,
                    line_number=i + 1
                )
            except LexingError as e:
                Logger.log_critical(f'{self._current_module.filepath}: {i + 1}: {e}')
                os.system('pause')
                exit(-1)

            self._tokens.append(create_token(
                token_type=TokenTypes.endline,
                text='\n',
                line=i + 1,
            ))

        return self._tokens


def create_lexer(module: Module) -> BaseLexer:
    """Lexer factory"""
    return import_class(LEXER_CLASS_PATH)(
        module=module,
    )
