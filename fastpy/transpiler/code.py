from abc import ABC, abstractmethod


class BaseCode(ABC):
    @abstractmethod
    def push_internal(self, code: str, **kwargs): ...

    @abstractmethod
    def push_external(self, code: str, **kwargs): ...

    @property
    @abstractmethod
    def internal(self) -> str: ...

    @property
    @abstractmethod
    def external(self) -> str: ...


class Code(BaseCode):
    def __init__(self):
        self._internal = ''
        self._external = ''

    def push_internal(self, code: str, **kwargs):
        auto_semicolon = kwargs.get('auto_semicolon', True)
        endl = kwargs.get('endl', True)

        if not code:
            return

        if auto_semicolon and not code.endswith(';'):
            if code.endswith('\n'):
                for char in reversed(code):
                    if char == ';':
                        break

                    elif char not in ('\n', ' '):
                        code += ';'
                        break

            else:
                code += ';'

        if endl:
            code += '\n'

        self._internal += code

    def push_external(self, code: str, **kwargs):
        auto_semicolon = kwargs.get('auto_semicolon', True)
        endl = kwargs.get('endl', False)

        if not code:
            return

        code = code.strip()

        if auto_semicolon and not code.endswith(';'):
            code += ';'

        if endl:
            code += '\n'
        self._external += code

    def __repr__(self):
        return self._internal

    @property
    def internal(self) -> str:
        return self._internal

    @property
    def external(self) -> str:
        return self._external
