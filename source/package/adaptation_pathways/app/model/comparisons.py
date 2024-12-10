from enum import Enum


class SequenceComparison(Enum):
    STARTS_WITH = 1
    DOESNT_START_WITH = 2
    CONTAINS = 3
    DOESNT_CONTAIN = 4
    ENDS_WITH = 5
    DOESNT_END_WITH = 6
    BLOCKS = 7
    AFTER = 8
    DIRECTLY_AFTER = 9
    BEFORE = 10
    DIRECTLY_BEFORE = 11


class NumberComparison(Enum):
    EQUAL = 1
    DOESNT_EQUAL = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL = 4
    GREATER_THAN = 5
    GREATER_THAN_OR_EQUAL = 6
