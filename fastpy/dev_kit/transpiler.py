from fastpy.filesystem import FileSystem as Fs
from fastpy.log import Logger
from fastpy.lexer import create_lexer, BaseToken
from fastpy.parser import create_parser, BaseAST
from fastpy.semantic_analyzer import create_analyzer
from fastpy.parser.nodes import CallNode
from fastpy.module import Module
from fastpy.transpiler import create_transpiler
from .config import BUILTIN_FUNCTIONS
from fastpy.exceptions import *


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

    @staticmethod
    def _analyze_file(module: Module, ast: BaseAST):
        analyzer = create_analyzer(
            module=module,
            ast=ast
        )
        analyzer.analyze()

    def _save_cpp_code(self, module: Module, code: str) -> str:
        out_folder = self.kwargs.get('output') or 'fastpy_build'
        Fs.makedirs(out_folder)
        out_folder = Fs.normalize_path(out_folder)
        Fs.makedirs(Fs.join(out_folder, 'bin'))
        Fs.makedirs(Fs.join(out_folder, 'src'))
        filepath = Fs.join(out_folder, 'src',
                           Fs.replace_ext(module.filename, '.cpp' if module.name == '__main__' else '.hpp'))
        Fs.write_file(filepath, code)
        Logger.log_info(f'Code saved to "{filepath}"')
        return filepath

    def _compile(self, main_cpp_file: str) -> str:
        out_folder = self.kwargs.get('output') or 'fastpy_build'
        out_bin_filepath = Fs.join(out_folder, 'bin', 'main.exe')
        command = f'g++ {Fs.normalize_path(main_cpp_file)} -o {out_bin_filepath} -std=c++1z'
        out_code = Fs.execute(command)
        if out_code == 0:
            Logger.log_info(f'Compilation complete, binaries saved to "{Fs.join(out_folder, "bin")}"')
        return out_bin_filepath

    def _transpile_file(self, module: Module) -> str:

        # first step: lexing
        tokens = self._lex_file(module)

        # second step: parsing
        ast = self._parse_file(module, tokens)

        # importing modules are processed after parsing
        for node in ast.nodes(module.name):
            if isinstance(node, CallNode):
                if node.identifier.text == BUILTIN_FUNCTIONS['import']:
                    for importing_file in node.arguments:
                        try:
                            importing_file = Fs.normalize_path(importing_file.value.text)
                            self._transpile_file(Module(importing_file))
                        except FileNotFoundError as e:
                            raise ParsingError('ImportError: ' + e.args[0].casefold())

        # third step: semantic analyzing
        self._analyze_file(module, ast)

        # fourth step: transpiling
        cpp_code = self._translate_file(module, ast)
        return self._save_cpp_code(module, cpp_code)

    def _copy_reqs(self):
        out_folder = self.kwargs.get('output') or 'fastpy_build'
        libs_folder = Fs.join(out_folder, 'src', 'include')
        Fs.makedirs(libs_folder)
        Fs.copy_files('cpp_code/libs', libs_folder)

    def transpile(self) -> str:
        main_cpp_file = self._transpile_file(Module(self.main_source_file, '__main__'))
        self._copy_reqs()
        if self.kwargs.get('compile', False):
            return self._compile(main_cpp_file)
        return main_cpp_file
