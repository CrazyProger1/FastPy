"""Additional tools for tokens validation"""

from ..lexer import BaseToken, TokenTypes


class Validators:
    """
    This class is just a wrapper for functions that are used for parsing
    """

    @staticmethod
    def check_token_type(tokens: list[BaseToken], token_index: int, possible_types: list[int | str]) -> bool:
        """

        :param tokens: list of tokens for check
        :param token_index: particular token index
        :param possible_types: possible types of particular token
        :return: some type matches with token name
        """

        token_type = tokens[token_index].type

        if isinstance(possible_types[0], str):
            return token_type.name in possible_types
        else:
            return token_type.value in possible_types

    @staticmethod
    def check_token_name(tokens: list[BaseToken], token_index: int, possible_names: list[str]) -> bool:
        """

        :param tokens: list of tokens for check
        :param token_index: particular token index
        :param possible_names: possible names of particular token
        :return: some name matches with token name
        """

        token_name = tokens[token_index].name
        return token_name in possible_names

    @staticmethod
    def check_token_type_presence(
            tokens: list[BaseToken],
            required_types: list[str | int | TokenTypes]
    ):
        """

        :param tokens: list of tokens for check
        :param required_types: types that must presence in the token list
        :return: present all required types
        """

        types = tuple(map(lambda t: t.type.name, tokens)) \
            if isinstance(required_types[0], str) \
            else tuple(map(lambda t: t.type.value, tokens))

        for required_type in required_types:
            if required_type not in types:
                return False
        return True

    @staticmethod
    def check_token_name_presence(tokens: list[BaseToken], required_names: list[str]):
        """

        :param tokens: list of tokens for check
        :param required_names: names that must presence in the token list
        :return: present all required names
        """

        names = tuple(map(lambda t: t.name, tokens))
        for required_name in required_names:
            if required_name not in names:
                return False
        return True

    @staticmethod
    def check_token_types(tokens: list[BaseToken], types: list[int]) -> bool:
        """

        :param tokens: list of tokens for check
        :param types: list of supposed token types in the same order as the tokens
        :return: match types
        """

        for token, supposed_type in zip(tokens, types):
            if supposed_type is None:
                continue

            if token.type != supposed_type:
                return False

        return True

    @staticmethod
    def check_token_texts(tokens: list[BaseToken], texts: list[str]) -> bool:
        """

        :param tokens: list of tokens for check
        :param texts: list of supposed token texts in the same order as the tokens
        :return: match texts
        """

        for token, supposed_text in zip(tokens, texts):
            if supposed_text is None:
                continue

            if token.text != supposed_text:
                return False

        return True

    @staticmethod
    def check_token_names(tokens: list[BaseToken], names: list[str]) -> bool:
        """

        :param tokens: list of tokens for check
        :param names: list of supposed token names in the same order as the tokens
        :return: match names
        """

        for token, supposed_name in zip(tokens, names):
            if supposed_name is None:
                continue

            if token.name != supposed_name:
                return False

        return True

    @staticmethod
    def check_min_tokens_length(tokens: list[BaseToken], min_length: int):
        """

        :param tokens: list of tokens for check
        :param min_length: min length of tokens list
        :return: len of tokens >= min length
        """
        return len(tokens) >= min_length

    @staticmethod
    def check_fixed_tokens_length(tokens: list[BaseToken], length: int):
        """

        :param tokens: list of tokens for check
        :param length: supposed length of tokens list
        :return: len of tokens == length
        """
        return len(tokens) == length
