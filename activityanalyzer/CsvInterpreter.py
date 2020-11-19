import re
import yaml
import copy
import pandas as pd

from activityanalyzer.logger import get_logger
from activityanalyzer.CsvParser import CsvParser
from activityanalyzer.Transaction import Transaction
from activityanalyzer.Balance import Balance


class CsvInterpreter:
    def __init__(self, csv_file_paths: iter, yaml_file_path: str):
        self._csv_file_paths = csv_file_paths
        self._yaml_file_path = yaml_file_path

        self._statements = []
        self._transactions = []
        self._balances = []

        self._column_names, self._format_context, self._default_values = self._parse_yaml_file()
        self._log = get_logger('CsvInterpreter.log', __name__)
        self._csv_parser = CsvParser(csv_file_paths, encoding=self._format_context['file_encoding'])
        self._parse_column_names()
        self._parse_statements()
        self._compute_balances()

    def _parse_yaml_file(self) -> tuple:
        with open(self._yaml_file_path, 'r', encoding='utf-8') as file:
            try:
                data = yaml.load(file, Loader=yaml.Loader)
                return data['ColumnNames'], data['FormatContext'], data['DefaultValues']
            except yaml.YAMLError as exc:
                print(exc)

    def _parse_column_names(self) -> None:
        column_names = self.get_column_names()
        for key, value in self._column_names.items():
            if value not in column_names:
                self._log.error("Unable to find '{}' column name in csv file. "
                                "Check the corresponding yaml config file.".format(value))
            else:
                self._column_names[key] = column_names.index(value)

    def _parse_statements(self) -> None:
        # Remove potential duplicates
        statement_rows = set()
        for row in self._csv_parser.get_row_generator(self._transaction_filter, self._balance_filter,
                                                      CsvParser.FilterLogic.OR):
            statement_rows.add(row)

        # Parse statement rows
        for row in statement_rows:
            if self._transaction_filter(row):
                el = Transaction(row, self._column_names, self._format_context)
                if el.amount > 0.0 and not el.principal_beneficiary:
                    el.principal_beneficiary = self._default_values['principal_beneficiary']
            else:
                el = Balance(row, self._column_names, self._format_context)
            self._statements.append(el)

        # Sort statements
        self._statements = sorted(self._statements, key=lambda el: el.get_date(), reverse=True)

        # Filter transactions
        self._transactions = [s for s in self._statements if isinstance(s, Transaction)]

    def _compute_balances(self) -> list:
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

    def get_column_names(self) -> tuple:
        new_row = None
        for row in self._csv_parser.get_row_generator():
            old_row, new_row = new_row, list(row)
            if self._transaction_filter(new_row) and len(old_row) == len(new_row):
                while not old_row[-1]:
                    old_row.pop()
                return old_row

    def get_transactions(self, pandas_dataframe=True) -> iter:
        if pandas_dataframe:
            return self._generate_dataframe(self._transactions)
        return self._transactions

    def get_earnings(self, pandas_dataframe=True) -> iter:
        earnings = [t for t in self._transactions if t.amount > 0.0]
        if pandas_dataframe:
            return self._generate_dataframe(earnings)
        return earnings

    def get_expenses(self, pandas_dataframe=True) -> iter:
        expenses = [t for t in self._transactions if t.amount < 0.0]
        if pandas_dataframe:
            return self._generate_dataframe(expenses)
        return expenses

    def get_balances(self, pandas_dataframe=True) -> iter:
        if pandas_dataframe:
            return self._generate_dataframe(self._balances)
        return self._balances

    @staticmethod
    def _generate_dataframe(obj_list: iter) -> pd.DataFrame:
        columns = list(obj_list[0].__dict__.keys())
        data = [list(obj.__dict__.values()) for obj in obj_list]
        df = pd.DataFrame(data, columns=columns)
        return df

    @staticmethod
    def _transaction_filter(row: tuple) -> bool:
        if row:
            return bool(re.match(r'^\d\d\.\d\d\.\d\d\d\d$', row[0]))
        return False

    @staticmethod
    def _balance_filter(row: tuple) -> bool:
        if row:
            return bool(re.match(r'^Kontostand vom.+$', row[0]))
        return False
