class BaseError(Exception):
    pass


class CompilationError(BaseError):
    pass


class LexingError(BaseError):
    pass


class ParsingError(BaseError):
    pass


class TranspilingError(BaseError):
    pass


