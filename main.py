import fastpy
import argparse
from config import *


def make_action(args: argparse.Namespace):
    if args.translate:
        fastpy.translate(**vars(args))


def setup_argparse() -> argparse.ArgumentParser:
    """Configuring the console argument parser"""
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
