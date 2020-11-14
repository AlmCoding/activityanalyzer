import re
from datetime import datetime

from activityanalyzer.helper import parse_amount, parse_date


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

    # def __lt__(self, other):
    #    return self.booking_date < other.booking_date

    def get_date(self):
        return self.value_date

    def parse(self, row: list, column_names: dict, format_context: dict):
        # self.booking_date = row[column_names['booking_date']]
        self.booking_date = parse_date(row[column_names['booking_date']], format_context)
        self.value_date = parse_date(row[column_names['value_date']], format_context)
        self.booking_text = row[column_names['booking_text']]
        self.principal_beneficiary = row[column_names['principal_beneficiary']]
        self.reference_line = row[column_names['reference_line']]
        self.account_number = row[column_names['account_number']]
        self.amount = parse_amount(row[column_names['amount']])

    def print(self):
        for key, value in self.__dict__.items():
            print('{}: {}'.format(key, value))
        print('')
