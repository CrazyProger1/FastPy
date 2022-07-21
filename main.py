import fastpy
import argparse
from config import *


def setup_argparse() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser(**ARGPARSE_CONFIG['parser'])

    for argument_config in ARGPARSE_CONFIG['arguments']:
        argparser.add_argument(*argument_config['args'], **argument_config['kwargs'])

    return argparser


def main():
    argparser = setup_argparse()
    parsed_args = argparser.parse_args()

    fastpy.lexer.Lexer('''
# Just a comment :D

log('Hello, World!') # print hello world
''').lex()  # TEST


if __name__ == '__main__':
    main()
