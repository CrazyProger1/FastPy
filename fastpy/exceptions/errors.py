class BaseError(Exception):
    pass


class ConfigNotLoadedError(BaseError):
    pass


class LexingError(BaseError):
    pass


class ParsingError(BaseError):
    pass


class TranspilingError(BaseError):
    pass


class CompilationError(BaseError):
    pass
