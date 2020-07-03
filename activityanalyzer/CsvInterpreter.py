import re
import yaml
import copy

from activityanalyzer.logger import get_logger
from activityanalyzer.CsvParser import CsvParser
from activityanalyzer.Transaction import Transaction
from activityanalyzer.Balance import Balance


class CsvInterpreter:
    def __init__(self, csv_file_paths: iter, yaml_file_path: str):
        self._csv_file_paths = csv_file_paths
        self._yaml_file_path = yaml_file_path

        self._statements = []
        self._balances = []

        self._column_names, self._format_context, self._default_values = self.parse_yaml_file()
        self._log = get_logger('CsvInterpreter.log', __name__)
        self._csv_parser = CsvParser(csv_file_paths, encoding=self._format_context['file_encoding'])
        self.parse_column_names()
        self.parse_statements()
        self.parse_balances()

    def parse_yaml_file(self) -> tuple:
        with open(self._yaml_file_path, 'r', encoding='utf-8') as file:
            try:
                data = yaml.load(file, Loader=yaml.Loader)
                return data['ColumnNames'], data['FormatContext'], data['DefaultValues']
            except yaml.YAMLError as exc:
                print(exc)

    def parse_statements(self) -> None:
        # Remove potential duplicates
        statement_rows = set()
        for row in self._csv_parser.get_row_generator(self.transaction_filter, self.balance_filter,
                                                      CsvParser.FilterLogic.OR):
            statement_rows.add(row)

        # Parse statement rows
        for row in statement_rows:
            if self.transaction_filter(row):
                el = Transaction(row, self._column_names, self._format_context)
                if el.amount > 0.0 and not el.principal_beneficiary:
                    el.principal_beneficiary = self._default_values['principal_beneficiary']
            else:
                el = Balance(row, self._column_names, self._format_context)
            self._statements.append(el)

        # Sort statements
        self._statements = sorted(self._statements, key=lambda el: el.get_date(), reverse=True)

    def parse_balances(self) -> list:
        balance_buffer = None
        for idx, statement in enumerate(self._statements):

            if isinstance(statement, Balance):
                if balance_buffer and abs(statement.amount - balance_buffer.amount) >= 0.01:
                    print("Missing transactions in time period from {} - {}"
                          .format(statement.date.date(), balance_buffer.date.date()))
                    # print("Insert artificial transaction for correcting sequence.")
                    # TODO Insert artificial transaction for correcting sequence.

                self._balances.append(copy.copy(statement))
                balance_buffer = copy.copy(statement)
                balance_buffer.decrement_date()
                continue
            elif not idx:
                Exception("Invalid statement list. Statement list must start with 'Balance' object.")

            while True:
                if self._balances[-1].date.replace(hour=0, minute=0) == statement.value_date.replace(hour=0, minute=0):
                    balance_buffer -= statement
                    break
                else:
                    self._balances.append(copy.copy(balance_buffer))
                    balance_buffer.decrement_date()

        return self._balances

    def get_balances(self) -> iter:
        return [s for s in self._statements if isinstance(s, Balance)]

    def get_transactions(self) -> iter:
        return [s for s in self._statements if isinstance(s, Transaction)]

    def get_earnings(self) -> iter:
        return [t for t in self.get_transactions() if t.amount > 0.0]

    def get_expenses(self) -> iter:
        return [t for t in self.get_transactions() if t.amount <= 0.0]

    def get_column_names(self) -> tuple:
        new_row = None
        for row in self._csv_parser.get_row_generator():
            old_row, new_row = new_row, list(row)
            if self.transaction_filter(new_row) and len(old_row) == len(new_row):
                while not old_row[-1]:
                    old_row.pop()
                return old_row

    def parse_column_names(self) -> None:
        column_names = self.get_column_names()
        for key, value in self._column_names.items():
            if value not in column_names:
                self._log.error("Unable to find '{}' column name in csv file. "
                                "Check the corresponding yaml config file.".format(value))
            else:
                self._column_names[key] = column_names.index(value)

    @staticmethod
    def transaction_filter(row: tuple) -> bool:
        if row:
            return bool(re.match(r'^\d\d\.\d\d\.\d\d\d\d$', row[0]))
        return False

    @staticmethod
    def balance_filter(row: tuple) -> bool:
        if row:
            return bool(re.match(r'^Kontostand vom.+$', row[0]))
        return False


"""
        # for row in sorted(transaction_rows, key=lambda row: row[0]):
"""

"""
def parse_transactions(self) -> None:
    # Remove potential duplicates
    transaction_rows = set()
    for row in self._csv_parser.get_row_generator(self.transaction_filter):
        transaction_rows.add(row)

    # Parse transaction rows
    for row in transaction_rows:
        t = Transaction(row, self._column_names, self._format_context)
        if t.amount > 0.0 and not t.principal_beneficiary:
            t.principal_beneficiary = self._default_values['principal_beneficiary']
        self.transactions.append(t)

    # Sort transactions
    self.transactions = sorted(self.transactions, key=lambda t: t.booking_date)

def parse_balances(self) -> None:
    balance_rows = set()
    for row in self._csv_parser.get_row_generator(self.balance_filter):
        balance_rows.add(row)

    # Parse balance rows
    for row in balance_rows:
        t = Transaction(row, self._column_names, self._format_context)
        self.balances.append(t)

    # Sort balances
    self.balances = sorted(self.balances, key=lambda t: t.booking_date)
"""