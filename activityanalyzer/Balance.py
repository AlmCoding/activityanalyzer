import re
from datetime import datetime, timedelta

from activityanalyzer.helper import parse_amount, parse_date


class Balance:
    def __init__(self, row: list, column_names: dict, format_context: dict):
        self.date = None
        self.amount = None
        self._parse(row, column_names, format_context)

    def __lt__(self, other):
        return self.date < other.date

    def __sub__(self, other):
        self.amount -= other.amount
        return self

    def get_date(self):
        return self.date

    def decrement_date(self, n=1):
        self.date -= timedelta(days=n)
        return self.date

    def print(self):
        for key, value in self.__dict__.items():
            print('{}: {}'.format(key, value))
        print('')

    def _parse(self, row: list, column_names: dict, format_context: dict):
        self.date = parse_date(re.search(r'\d\d\.\d\d\.\d\d\d\d', row[0]).group(0), format_context,
                               time_delta={'hours': 23, 'minutes': 59})
        self.amount = parse_amount(row[1].split(' ')[0])
