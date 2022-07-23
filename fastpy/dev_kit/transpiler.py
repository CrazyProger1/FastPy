from fastpy.filesystem import FileSystem as Fs
from fastpy.log import Logger
from fastpy.lexer import create_lexer
from fastpy.parser import create_parser, BaseAST, ImportNode


class Transpiler:
    def __init__(self, source: str, **kwargs):
        self.main_source_file = source
        self.kwargs = kwargs

    def _transpile_file(self, source_file: str, module: str = '__main__') -> str:
        # first step: lexing
        source_file = Fs.normalize_path(source_file)
        source_code = Fs.read_file(source_file)
        lexer = create_lexer(source_code)
        tokens = lexer.lex()
        Logger.print_raw('|'.join(map(str, tokens)), 'TOKENS:')

        # second step: parsing
        parser = create_parser(tokens, module)
        ast = parser.parse()
        Logger.print_raw(ast, 'ABSTRACT SYNTAX TREE:')

        # importing modules are processed after parsing
        for node in ast.module_nodes(module):
            if isinstance(node, ImportNode):
                importing_file = node.filepath.text
                self._transpile_file(importing_file, Fs.get_name(importing_file))

        # third step: transpiling

    def transpile(self) -> str:
        return self._transpile_file(self.main_source_file, '__main__')
