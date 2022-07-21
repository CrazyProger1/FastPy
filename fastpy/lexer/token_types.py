from enum import Enum


class TokenTypes(Enum):
    endline = 1
    operator = 2
    identifier = 3
    literal = 4
    comma = 5
    start_parenthesis = 6
    end_parenthesis = 7
    gap = 8
    number = 9

    def __eq__(self, other):
        if isinstance(other, int):
            return self.endline == other
        return super(TokenTypes, self).__eq__(other)
