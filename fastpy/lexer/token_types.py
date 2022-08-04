from enum import Enum


class TokenTypes(Enum):
    operator = 1
    identifier = 2
    literal = 3
    comma = 4
    start_parenthesis = 5
    end_parenthesis = 6
    start_braces = 7
    end_braces = 8
    start_square = 9
    end_square = 10
    gap = 11
    tab = 12
    number = 13
    endline = 14
    start_chevrons = 15
    end_chevrons = 16

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, str):
            return self.name == other

        return super(TokenTypes, self).__eq__(other)
