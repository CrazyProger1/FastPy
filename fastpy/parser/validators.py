"""Additional tools for tokens validation"""
from ..lexer import BaseToken


class Validators:
    @staticmethod
    def check_token_type(tokens: list[BaseToken], token_index: int, possible_types: list[int | str]) -> bool:
        token_type = tokens[token_index].type

        if isinstance(possible_types[0], str):
            return token_type.name in possible_types
        else:
            return token_type.value in possible_types

    @staticmethod
    def check_token_name(tokens: list[BaseToken], token_index: int, possible_names: list[str]) -> bool:
        token_name = tokens[token_index].name
        return token_name in possible_names

    @staticmethod
    def check_tokens_types(tokens: list[BaseToken], types: list[int]) -> bool:
        for token, supposed_type in zip(tokens, types):
            if supposed_type is None:
                continue

            if token.type != supposed_type:
                return False

        return True

    @staticmethod
    def check_tokens_texts(tokens: list[BaseToken], texts: list[str]) -> bool:
        for token, supposed_text in zip(tokens, texts):
            if supposed_text is None:
                continue

            if token.text != supposed_text:
                return False

        return True

    @staticmethod
    def check_tokens_names(tokens: list[BaseToken], names: list[str]) -> bool:
        for token, supposed_name in zip(tokens, names):
            if supposed_name is None:
                continue

            if token.name != supposed_name:
                return False

        return True

    @staticmethod
    def check_min_tokens_length(tokens: list[BaseToken], min_length: int):
        return len(tokens) >= min_length

    @staticmethod
    def check_fixed_tokens_length(tokens: list[BaseToken], length: int):
        return len(tokens) == length
