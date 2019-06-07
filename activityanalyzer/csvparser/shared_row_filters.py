import enum
import re





class RowSizeFilter:
    class Match(enum.Enum):
        SHORTER = 0
        SHORTER_EQUAL = 1
        EQUAL = 2
        LONGER_EQUAL = 3
        LONGER = 4

    def __init__(self, match, size):
        self._match = match
        self._size = size

    def filter(self, row):
        if self._match == RowSizeFilter.Match.SHORTER:
            return len(row) < self._size
        elif self._match == RowSizeFilter.Match.SHORTER_EQUAL:
            return len(row) <= self._size
        elif self._match == RowSizeFilter.Match.EQUAL:
            return len(row) == self._size
        elif self._match == RowSizeFilter.Match.LONGER_EQUAL:
            return len(row) >= self._size
        elif self._match == RowSizeFilter.Match.LONGER:
            return len(row) > self._size


class ExactRowMatchFilter:
    def __init__(self, match):
        self._match = [col.strip() for col in match if match]

    def filter(self, row):
        row = [col for col in row if col]
        if RowSizeFilter(RowSizeFilter.Match.EQUAL, len(row)):
            return row == self._match


