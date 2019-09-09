import re
import yaml

from activityanalyzer.logger import get_logger
from activityanalyzer.CsvParser import CsvParser
from activityanalyzer.Transaction import Transaction


class CsvInterpreter:
    def __init__(self, csv_file_paths: iter, yaml_file_path: str):
        self._csv_file_paths = csv_file_paths
        self._yaml_file_path = yaml_file_path

        self.transactions = []

        self._column_names, self._format_context = self.parse_yaml_file()
        self._log = get_logger('CsvInterpreter.log', __name__)
        self._csv_parser = CsvParser(csv_file_paths, encoding=self._format_context['file_encoding'])
        self.parse_column_names()
        self.parse_transactions()

    def parse_yaml_file(self) -> list:
        with open(self._yaml_file_path, 'r', encoding='utf-8') as file:
            try:
                data = yaml.load(file, Loader=yaml.Loader)
                return [data['ColumnNames'], data['FormatContext']]
            except yaml.YAMLError as exc:
                print(exc)

    def parse_transactions(self) -> None:
        transaction_rows = set()
        for row in self._csv_parser.get_row_generator(self.transaction_filter):
            transaction_rows.add(row)

        for row in sorted(transaction_rows, key=lambda row: row[0]):
            t = Transaction(row, self._column_names, self._format_context)
            if t.amount > 0.0 and not t.principal_beneficiary:
                t.principal_beneficiary = 'Cash Deposit'
            self.transactions.append(t)

    """
    def get_transactions(self) -> iter:
        for row in self._csv_parser.get_row_generator(self.transaction_filter):
            t = Transaction(row, self._column_names, self._format_context)
            if t.amount > 0.0 and not t.principal_beneficiary:
                t.principal_beneficiary = 'Cash Deposit'
            yield t
    """

    def get_earnings(self) -> iter:
        for t in self.transactions:
            if t.amount > 0.0:
                yield t

    def get_expenses(self) -> iter:
        for t in self.transactions:
            if t.amount < 0.0:
                yield t

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
            return bool(re.match(r'^(\d\d\.\d\d\.\d\d\d\d)$', row[0]))
        return False


if __name__ == '__main__':
    csv_file = '../data/dkb_2018.csv'
    yaml_file = 'DeutscheKreditbank.yaml'

    import os
    print(os.listdir('.'))

    interpreter = CsvInterpreter(csv_file, yaml_file)
    gen = interpreter.get_transactions()
