import fastpy
import argparse
from config import *


def make_action(args: argparse.Namespace):
    """Performs actions such as transpiling or compiling depending on the input"""
    if args.translate:
        fastpy.TranspileAPI(**vars(args)).transpile()


def setup_argparse() -> argparse.ArgumentParser:
    """Configures the console argument parser"""
    argparser = argparse.ArgumentParser(**ARGPARSE_CONFIG['parser'])

    for argument_config in ARGPARSE_CONFIG['arguments']:
        argparser.add_argument(*argument_config['args'], **argument_config['kwargs'])

    return argparser


def main():
    argparser = setup_argparse()
    parsed_args = argparser.parse_args()
    make_action(parsed_args)


if __name__ == '__main__':
    main()
