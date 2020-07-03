import re
from datetime import datetime, timedelta


class Balance:
    def __init__(self, row: list, column_names: dict, format_context: dict):
        self.date = None
        self.amount = None
        self.parse(row, column_names, format_context)

    def __lt__(self, other):
        return self.date < other.date

    def __sub__(self, other):
        self.amount -= other.amount
        return self

    def get_date(self):
        return self.date

    def parse(self, row: list, column_names: dict, format_context: dict):
        self.date = Balance.parse_date(re.search(r'\d\d\.\d\d\.\d\d\d\d', row[0]).group(0), format_context)
        self.amount = Balance.parse_amount(row[1].split(' ')[0])

    # def init_

    def print(self):
        for key, value in self.__dict__.items():
            print('{}: {}'.format(key, value))
        print('')

    @staticmethod
    def parse_amount(amount: str) -> float:
        separators = re.findall(r'[^\d]', amount)
        decimal_separator = separators[-1]
        thousands_separator = ',' if decimal_separator == '.' else '.'
        amount = amount.replace(thousands_separator, '')
        amount = amount.replace(decimal_separator, '.')
        return float(amount)

    @staticmethod
    def parse_date(date, format_context):
        date_format = format_context['date']
        return datetime.strptime(date, date_format) + timedelta(hours=23, minutes=59)

    def decrement_date(self, n=1):
        self.date -= timedelta(days=n)
        return self.date
