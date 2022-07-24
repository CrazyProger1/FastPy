from fastpy.filesystem import FileSystem as Fs
from fastpy.log import Logger
from fastpy.lexer import create_lexer
from fastpy.parser import create_parser, BaseAST, ImportNode
from fastpy.module import Module


class TranspileAPI:
    def __init__(self, source: str, **kwargs):
        self.main_source_file = Fs.normalize_path(source)
        self.kwargs = kwargs

    def _transpile_file(self, module: Module) -> str:

        # first step: lexing
        lexer = create_lexer(
            module=module
        )

        tokens = lexer.lex()
        Logger.print_raw('|'.join(map(str, tokens)), 'TOKENS:')

        # second step: parsing
        parser = create_parser(
            module=module,
            tokens=tokens
        )

        ast = parser.parse()
        Logger.print_raw(ast, 'ABSTRACT SYNTAX TREE:')

        # importing modules are processed after parsing
        for node in ast.module_nodes(module.name):
            if isinstance(node, ImportNode):
                importing_file = Fs.normalize_path(node.filepath.text)
                self._transpile_file(Module(importing_file))

        # third step: transpiling

    def transpile(self) -> str:
        return self._transpile_file(Module(self.main_source_file, '__main__'))
