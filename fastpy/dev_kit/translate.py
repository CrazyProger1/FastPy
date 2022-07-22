from fastpy.filesystem import FileSystem as Fs
from fastpy.log import Logger
from fastpy.lexer import create_lexer
from fastpy.parser import create_parser


def translate(source: str, **kwargs) -> str:
    # first step: lexing
    source = Fs.normalize_path(source)
    source_code = Fs.read_file(source)
    lexer = create_lexer(source_code)
    tokens = lexer.lex()
    Logger.print_raw('|'.join(map(str, tokens)), 'TOKENS:')

    # second step: parsing
    parser = create_parser(tokens)
    ast = parser.parse()
    Logger.print_raw(ast, 'ABSTRACT SYNTAX TREE:')

    # third step: transpiling
