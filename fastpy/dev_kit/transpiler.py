from fastpy.filesystem import FileSystem as Fs
from fastpy.log import Logger
from fastpy.lexer import create_lexer, BaseToken
from fastpy.parser import create_parser, BaseAST, ImportNode
from fastpy.module import Module
from fastpy.transpiler import create_transpiler


class TranspileAPI:
    def __init__(self, source: str, **kwargs):
        self.main_source_file = Fs.normalize_path(source)
        self.kwargs = kwargs

    @staticmethod
    def _lex_file(module: Module) -> list[BaseToken]:
        lexer = create_lexer(
            module=module
        )

        tokens = lexer.lex()
        Logger.print_raw('|'.join(map(str, tokens)), 'TOKENS:')
        return tokens

    @staticmethod
    def _parse_file(module: Module, tokens: list[BaseToken]) -> BaseAST:
        parser = create_parser(
            module=module,
            tokens=tokens
        )

        ast = parser.parse()
        Logger.print_raw(ast, 'ABSTRACT SYNTAX TREE:')
        return ast

    @staticmethod
    def _translate_file(module: Module, ast: BaseAST) -> str:
        transpiler = create_transpiler(
            module=module,
            ast=ast
        )
        cpp_code = transpiler.transpile()
        Logger.print_raw(cpp_code, 'CPP CODE:')
        return cpp_code

    def _transpile_file(self, module: Module) -> str:

        # first step: lexing
        tokens = self._lex_file(module)

        # second step: parsing
        ast = self._parse_file(module, tokens)

        # importing modules are processed after parsing
        for node in ast.nodes(module.name):
            if isinstance(node, ImportNode):
                importing_file = Fs.normalize_path(node.filepath.text)
                self._transpile_file(Module(importing_file))

        # third step: transpiling
        cpp_code = self._translate_file(module, ast)

    def transpile(self) -> str:
        return self._transpile_file(Module(self.main_source_file, '__main__'))
