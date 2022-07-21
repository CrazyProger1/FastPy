from enum import Enum


class TokenTypes(Enum):
    endline = 1
    operator = 2
    identifier = 3
    literal = 4
    comma = 5
    start_parenthesis = 6
    end_parenthesis = 7
    start_braces = 8
    end_braces = 9
    start_square = 10
    end_square = 11
    gap = 12
    tab = 13
    number = 14

    def __eq__(self, other):
        if isinstance(other, int):
            return self.endline == other
        return super(TokenTypes, self).__eq__(other)
