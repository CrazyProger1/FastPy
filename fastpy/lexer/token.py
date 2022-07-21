from .token_types import TokenTypes


class Token:
    def __init__(self, token_type: TokenTypes, text: str, line: int, name: str = None):
        self._type = token_type
        self._text = text
        self._line = line
        self._name = name

    @property
    def type(self) -> TokenTypes:
        return self._type

    @property
    def text(self) -> str:
        return self._text

    @property
    def line(self) -> int:
        return self._line

    @property
    def name(self) -> str | None:
        return self._name
