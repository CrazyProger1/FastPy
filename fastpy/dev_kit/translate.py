from fastpy.filesystem import FileSystem as Fs
from fastpy.log import Logger
from fastpy.lexer import lex_code


def translate(source: str, **kwargs) -> str:
    source = Fs.normalize_path(source)
    source_code = Fs.read_file(source)
    tokens = lex_code(source_code)
    Logger.print_raw(tokens, 'TOKENS:')
