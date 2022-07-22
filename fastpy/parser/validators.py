"""Additional tools for tokens validation"""
from ..lexer import BaseToken


def check_token_types(tokens: list[BaseToken], types: list[int]) -> bool:
    for token, supposed_type in zip(tokens, types):
        if supposed_type is None:
            continue

        if token.type != supposed_type:
            return False

    return True


def check_token_texts(tokens: list[BaseToken], texts: list[str]) -> bool:
    for token, supposed_text in zip(tokens, texts):
        if supposed_text is None:
            continue

        if token.text != supposed_text:
            return False

    return True


def check_token_names(tokens: list[BaseToken], names: list[str]) -> bool:
    for token, supposed_name in zip(tokens, names):
        if supposed_name is None:
            continue

        if token.name != supposed_name:
            return False

    return True
