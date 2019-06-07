from datetime import datetime
import re


class Transaction:
    def __init__(self, row, column_names, format_context):
        self._booking_date = booking_date
        self._value_date = value_date
        self._booking_text = booking_text
        self._principal_beneficiary = principal_beneficiary
        self._reference_line = reference_line
        self._account_number = account_number
        self._amount = Transaction.parse_amount(amount)

    @staticmethod
    def parse_amount(amount):
        separators = re.findall(r'[^\d]', amount)
        decimal_separator = separators[-1]
        thousands_separator = ',' if decimal_separator == '.' else '.'
        amount = amount.replace(thousands_separator, '').replace(decimal_separator, '.')
        return float(amount)

    @staticmethod
    def parse_date(date):
        return datetime.strptime(date, '%d.%m.%Y').date()