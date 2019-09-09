import re
from datetime import datetime


class Transaction:
    def __init__(self, row: list, column_names: dict, format_context: dict):
        self.booking_date = None
        self.value_date = None
        self.booking_text = None
        self.principal_beneficiary = None
        self.reference_line = None
        self.account_number = None
        self.amount = None
        self.parse(row, column_names, format_context)

    def parse(self, row: list, column_names: dict, format_context: dict):
        self.booking_date = row[column_names['booking_date']]
        self.value_date = Transaction.parse_date(row[column_names['value_date']], format_context)
        self.booking_text = row[column_names['booking_text']]
        self.principal_beneficiary = row[column_names['principal_beneficiary']]
        self.reference_line = row[column_names['reference_line']]
        self.account_number = row[column_names['account_number']]
        self.amount = Transaction.parse_amount(row[column_names['amount']])

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
        return datetime.strptime(date, date_format).date()
